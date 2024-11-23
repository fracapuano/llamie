from fastapi import FastAPI, WebSocket
from typing import Optional
from dataclasses import dataclass

import os 
import sys

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(".")

from llami.robot.robot_router import run_policy
from lerobot.common.robot_devices.robots.factory import make_robot
from lerobot.common.robot_devices.robots.utils import Robot
from lerobot.common.utils.utils import init_hydra_config

@dataclass
class RobotConnection:
    robot: Robot
    active: bool = False

class RobotServer:
    def __init__(self, robot_config_path: Optional[str] = None):
        self.robot_config_path = robot_config_path if robot_config_path else "llami/configs/robot/moss.yaml"
        self.app = FastAPI()
        
        self.robot = make_robot(
            init_hydra_config(self.robot_config_path)
        )
        self.robot.connect()

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

if __name__ == "__main__":
    import uvicorn

    server = RobotServer()
    uvicorn.run(server.app, host="localhost", port=8080)