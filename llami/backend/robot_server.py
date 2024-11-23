from fastapi import FastAPI, WebSocket
from typing import Optional
from dataclasses import dataclass
from llami.configs.policy_extraction_prompt import get_extraction_prompt

import os 
import sys
import subprocess

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(".")

from llami.robot.robot_router import run_policy
from lerobot.common.robot_devices.robots.factory import make_robot
from lerobot.common.robot_devices.robots.utils import Robot
from lerobot.common.utils.utils import init_hydra_config

from pydantic import BaseModel

@dataclass
class RobotConnection:
    robot: Robot
    active: bool = False

@dataclass
class LlamaRequest(BaseModel):
    prompt: str

class RobotServer:
    def __init__(self, robot_config_path: Optional[str] = None):
        self.robot_config_path = robot_config_path if robot_config_path else "llami/configs/robot/moss.yaml"
        self.app = FastAPI()
        
        self.robot = make_robot(
            init_hydra_config(self.robot_config_path)
        )
        self.robot.connect()
        self.policy_extraction_prompt = get_extraction_prompt

        # this sets up the app routes
        self.setup_routes()
        
    def setup_routes(self):
        @self.app.on_event("startup")
        async def startup():
            """Initialize robot on server startup"""
            return {"status": "Robot connected"}

        @self.app.on_event("shutdown")
        async def shutdown():
            """Cleanup robot connection on server shutdown"""
            if self.robot and self.robot.is_connected:
                self.robot.disconnect()
            return {"status": "Robot disconnected"}

        @self.app.get("/execute_policy/{policy_name}")
        async def execute_policy(policy_name: str):
            """Execute a given robot policy"""
            run_policy(
                robot=self.robot,
                policy_name=policy_name
            )
            return {"status": f"Executing policy: {policy_name}"}

        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            """Optional WebSocket endpoint if you still need real-time communication"""
            await websocket.accept()
            try:
                while True:
                    policy_name = await websocket.receive_text()
                    run_policy(
                        robot=self.robot,
                        policy_name=policy_name
                    )
                    await websocket.send_json({"status": f"Executed policy: {policy_name}"})
            except Exception:
                await websocket.close()
        
        @self.app.post("/llama")
        async def llama(request: LlamaRequest):
            # augments the prompt with the user input
            prompt = self.policy_extraction_prompt(request.prompt)
            # binaries for the llama model
            directory = "llami/backend/models/"
            binary_llama = directory+"llama_main_xnnpack_arm"
            model_weights = directory+"llama3_2_xnn.pte"
            tokenizer = directory+"tokenizer.model"
            command = [binary_llama, "--model_path", model_weights, "--tokenizer_path", tokenizer, "--prompt", request.prompt]
            text = subprocess.run(command, capture_output=True).stdout
            
            policy_name = self.extract_policy(text)
            
            run_policy(
                robot=self.robot,
                policy_name=policy_name
            )
            
            return {"status": "ok"}
        
    def available_policies():
        """
        Return the list of available policies in configs/trained_policies
        """
        directory = "llami/configs/trained_policies/"
        return [f.name[:-5] for f in os.scandir(directory) if f.name.endswith(".yaml")]

    def extract_answer_from_llama_output(output: str):
        """
        Some additional information is printed after the answer, we need to remove it (performance metrics, etc.)
        """
        eot_id = output.find("PyTorchObserver")
        return output[:eot_id]

    # Process the text to extract the policy
    def extract_policy(self, text: str):
        available_policies = self.available_policies()

        # Easy version supposing all policies are of the form "grab_object"
        objects = [policy.split("_")[1] for policy in available_policies]
        for ind, object in enumerate(objects):
            if object in text:
                return available_policies[ind]
        
        # Actually we should rerun Llama if no policy is found
        return available_policies[0]  # Default policy


if __name__ == "__main__":
    import uvicorn

    server = RobotServer()
    uvicorn.run(server.app, host="localhost", port=8080)