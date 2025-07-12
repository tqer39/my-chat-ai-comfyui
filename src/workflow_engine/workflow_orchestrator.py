import asyncio
import json
from typing import Dict, Any, Optional
from loguru import logger

class WorkflowOrchestrator:
    def __init__(self, comfyui_client):
        self.comfyui_client = comfyui_client
        self.workflow_templates = self._load_workflow_templates()

    def _load_workflow_templates(self) -> Dict[str, Any]:
        return {
            "basic_generation": {
                "1": {
                    "class_type": "CheckpointLoaderSimple",
                    "inputs": {
                        "ckpt_name": "sd3.5_medium.safetensors"
                    }
                },
                "2": {
                    "class_type": "CLIPTextEncode",
                    "inputs": {
                        "text": "{prompt}",
                        "clip": ["1", 1]
                    }
                },
                "3": {
                    "class_type": "CLIPTextEncode",
                    "inputs": {
                        "text": "blurry, low quality, distorted",
                        "clip": ["1", 1]
                    }
                },
                "4": {
                    "class_type": "KSampler",
                    "inputs": {
                        "seed": 42,
                        "steps": 28,
                        "cfg": 4.5,
                        "sampler_name": "dpmpp_2m",
                        "scheduler": "normal",
                        "denoise": 1.0,
                        "model": ["1", 0],
                        "positive": ["2", 0],
                        "negative": ["3", 0],
                        "latent_image": ["5", 0]
                    }
                },
                "5": {
                    "class_type": "EmptyLatentImage",
                    "inputs": {
                        "width": 1024,
                        "height": 1024,
                        "batch_size": 1
                    }
                },
                "6": {
                    "class_type": "VAEDecode",
                    "inputs": {
                        "samples": ["4", 0],
                        "vae": ["1", 2]
                    }
                },
                "7": {
                    "class_type": "SaveImage",
                    "inputs": {
                        "filename_prefix": "chat_ai_generated",
                        "images": ["6", 0]
                    }
                }
            },
            "nsfw_filtered_generation": {
                "1": {
                    "class_type": "CheckpointLoaderSimple",
                    "inputs": {
                        "ckpt_name": "sd3.5_medium.safetensors"
                    }
                },
                "2": {
                    "class_type": "CLIPTextEncode",
                    "inputs": {
                        "text": "{prompt}",
                        "clip": ["1", 1]
                    }
                },
                "3": {
                    "class_type": "CLIPTextEncode",
                    "inputs": {
                        "text": "blurry, low quality, distorted, nsfw, explicit",
                        "clip": ["1", 1]
                    }
                },
                "4": {
                    "class_type": "KSampler",
                    "inputs": {
                        "seed": 42,
                        "steps": 28,
                        "cfg": 4.5,
                        "sampler_name": "dpmpp_2m",
                        "scheduler": "normal",
                        "denoise": 1.0,
                        "model": ["1", 0],
                        "positive": ["2", 0],
                        "negative": ["3", 0],
                        "latent_image": ["5", 0]
                    }
                },
                "5": {
                    "class_type": "EmptyLatentImage",
                    "inputs": {
                        "width": 1024,
                        "height": 1024,
                        "batch_size": 1
                    }
                },
                "6": {
                    "class_type": "VAEDecode",
                    "inputs": {
                        "samples": ["4", 0],
                        "vae": ["1", 2]
                    }
                },
                "7": {
                    "class_type": "NudenetModelLoader",
                    "inputs": {}
                },
                "8": {
                    "class_type": "ApplyNudenet",
                    "inputs": {
                        "image": ["6", 0],
                        "model": ["7", 0],
                        "confidence": 0.7,
                        "censoring_method": "blur"
                    }
                },
                "9": {
                    "class_type": "SaveImage",
                    "inputs": {
                        "filename_prefix": "chat_ai_filtered",
                        "images": ["8", 0]
                    }
                }
            }
        }

    async def execute_generation(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        try:
            logger.info(f"Executing generation with parameters: {parameters}")

            template_name = "nsfw_filtered_generation" if parameters.get("nsfw_filter", False) else "basic_generation"
            workflow = self._create_workflow_from_template(template_name, parameters)

            prompt_id = await self.comfyui_client.queue_prompt(workflow)
            if not prompt_id:
                return {"error": "Failed to queue prompt"}

            result = await self._wait_for_completion(prompt_id)
            return result

        except Exception as e:
            logger.error(f"Error executing generation: {e}")
            return {"error": str(e)}

    def _create_workflow_from_template(self, template_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        template = self.workflow_templates.get(template_name, self.workflow_templates["basic_generation"])
        workflow = json.loads(json.dumps(template))

        prompt = parameters.get("prompt", "a beautiful landscape")

        for node_id, node in workflow.items():
            if node.get("class_type") == "CLIPTextEncode" and "{prompt}" in str(node.get("inputs", {})):
                node["inputs"]["text"] = node["inputs"]["text"].replace("{prompt}", prompt)

        return workflow

    async def _wait_for_completion(self, prompt_id: str, timeout: int = 300) -> Dict[str, Any]:
        start_time = asyncio.get_event_loop().time()

        while True:
            if asyncio.get_event_loop().time() - start_time > timeout:
                return {"error": "Timeout waiting for completion"}

            history = await self.comfyui_client.get_history(prompt_id)

            if prompt_id in history:
                prompt_history = history[prompt_id]
                if "outputs" in prompt_history:
                    logger.success(f"Generation completed for prompt {prompt_id}")
                    return {
                        "success": True,
                        "prompt_id": prompt_id,
                        "outputs": prompt_history["outputs"]
                    }

            await asyncio.sleep(2)
