from fastapi import FastAPI, WebSocket
from typing import Optional
from dataclasses import dataclass

import os 
import sys
import subprocess
import ssl
from pathlib import Path

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(".")

from llami.configs.policy_extraction_prompt import get_extraction_prompt
from llami.robot.robot_router import run_policy
from lerobot.common.robot_devices.robots.factory import make_robot
from lerobot.common.robot_devices.robots.utils import Robot
from lerobot.common.utils.utils import init_hydra_config

from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


origins = [
    "*"
]


@dataclass
class RobotConnection:
    robot: Robot
    active: bool = False

@dataclass
class LlamaRequest(BaseModel):
    prompt: str

def available_policies():
    """
    Return the list of available policies in configs/trained_policies
    """
    directory = "llami/configs/trained_policies/"
    return [f.name[:-5] for f in os.scandir(directory) if f.name.endswith(".yaml")]


class RobotServer:
    def __init__(self, robot_config_path: Optional[str] = None):
        self.robot_config_path = robot_config_path if robot_config_path else "llami/configs/robot/moss.yaml"
        self.app = FastAPI()

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        self.robot = make_robot(
            init_hydra_config(self.robot_config_path)
        )
        self.robot.connect()
        self.policy_extraction_prompt = get_extraction_prompt

        # Add SSL configuration
        self.ssl_keyfile = "key.pem"
        self.ssl_certfile = "cert.pem"
        self.check_or_create_ssl_certificates()

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
        
        @self.app.get("/")
        async def root():
            return {"status": "ok"}

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
            command = [
                binary_llama, 
                "--model_path", 
                model_weights, 
                "--tokenizer_path", 
                tokenizer, 
                "--prompt", 
                prompt
            ]
            text = subprocess.run(command, capture_output=True).stdout

            policy_name = self.extract_policy(text)

            run_policy(
                robot=self.robot,
                policy_name=policy_name
            )
            
            return {"status": "ok"}
        
    def extract_answer_from_llama_output(output: str):
        """
        Some additional information is printed after the answer, we need to remove it (performance metrics, etc.)
        """
        eot_id = output.find("PyTorchObserver")
        return output[:eot_id]

    # Process the text to extract the policy
    def extract_policy(self, text: bytes):
        text = text.decode("utf-8")
        policies = available_policies()

        # Easy version supposing all policies are of the form "grab_object"
        objects = [policy.split("_")[1] for policy in policies]
        for ind, object in enumerate(objects):
            if object in text:
                return policies[ind]
        
        # Actually we should rerun Llama if no policy is found
        return policies[0]  # Default policy

    def check_or_create_ssl_certificates(self):
        """Create self-signed certificates if they don't exist"""
        if not (Path(self.ssl_keyfile).exists() and Path(self.ssl_certfile).exists()):
            subprocess.run([
                'openssl', 'req', '-x509', '-newkey', 'rsa:4096', '-nodes',
                '-out', self.ssl_certfile,
                '-keyout', self.ssl_keyfile,
                '-days', '365',
                '-subj', '/CN=localhost'
            ])


if __name__ == "__main__":
    import uvicorn

    server = RobotServer()
    uvicorn.run(
        server.app, 
        host="0.0.0.0", 
        port=8443,  # Standard HTTPS port
        ssl_keyfile=server.ssl_keyfile,
        ssl_certfile=server.ssl_certfile
    )