# LLami 🦙🦾🔈

**For <200$, control a Robot arm with your voice using Whisper and Llama on device.**  
_On-device, edge-powered AI/ML for real-time robotic control._

<div align="center">
  <a href="https://svelte.dev"><img src="https://img.shields.io/badge/Svelte-JS-orange" alt="Svelte"></a>
  <a href="https://huggingface.co/docs/transformers.js"><img src="https://img.shields.io/badge/Transformers.js-WASM-blue" alt="Transformers.js"></a>
  <a href="https://bun.sh"><img src="https://img.shields.io/badge/Bun-JS-black" alt="Bun"></a>
  <a href="https://github.com/huggingface/lerobot"><img src="https://img.shields.io/badge/LeRobot-HuggingFace-yellow" alt="HuggingFace"></a>
  <a href="https://fastapi.tiangolo.com"><img src="https://img.shields.io/badge/FastAPI-Python-green" alt="FastAPI"></a>
</div>

---

## About the Project 🌟

LLami is a voice-controlled robot arm built on a shoestring budget and powered by cutting-edge edge AI technologies. It’s simple, hacky, and fast—created in under **2 days** as a passion project by a small team of robotics and AI enthusiasts.

### Features 🚀

- **Voice Commands**: Speak, and the robot arm obeys! Powered by Whisper for real-time voice recognition.
- **Multi-device Compatibility**: Runs seamlessly on low-power devices (Jetson Nano, laptops, smartphones).
- **Edge AI/ML**: No cloud dependency—privacy and speed, all on-device.
- **Open Source Components**: Built on open technologies, including HuggingFace's LeRobot library and Transformers.js.

---

## Tech Stack 🛠️

| Technology          | Role                                                             |
| ------------------- | ---------------------------------------------------------------- |
| **Svelte**          | Smooth, responsive frontend for controlling the arm.             |
| **Transformers.js** | Voice processing with WebGPU acceleration (Whisper, Llama).      |
| **Bun**             | Blazing-fast JavaScript runtime for modern web projects.         |
| **LeRobot Library** | Hardware interface for LeRobot arm, thanks to HuggingFace.       |
| **FastAPI**         | Backend API for connecting voice recognition and robot commands. |

---

## Usage ⚡

> **Warning**: This project is a prototype. The code is messy, unoptimized, and not production-ready. Use at your own risk!

### Setup Instructions 🧰

1. Clone this repository:

   ```bash
   git clone https://github.com/your-repo/LLami
   cd LLami
   ```

2. Install dependencies for the backend:

   ```bash
   pip install -e .
   ```

   Don't forget to install lerobot from source :

   ```bash
   git clone https://github.com/huggingface/lerobot.git
   ```

   ```bash
   cd lerobot
   ```

   ```bash
   pip install -e .
   ```

3. Install frontend dependencies:

   ```bash
   cd frontend
   ```

   ```bash
   bun install
   ```

4. Start the backend server:

   ```bash
   python llami/backend/robot_server.py
   ```

5. Run the frontend:

   ```bash
   bun dev
   ```

6. Connect your LeRobot arm and start issuing voice commands! 🎙️

---

## Meet the Team 🧑‍💻

- **Francesco Capuano**
- **Thomas Loux**
- **Eyal Benaroche**
- **Giuseppe Suriano**

---

## Acknowledgments ❤️

- Big thanks to [HuggingFace](https://huggingface.co) 🤗 for the LeRobot library and Transformers.js and lending the arm.

---

## Disclaimer ⚠️

This project was built in **under 2 days** as a hackathon-style experiment. Expect rough edges, experimental code, and potential bugs. Contributions and improvements are welcome!
There is a `DOCKERFILE` for deployement of the frontend if you want to (defenitly not production ready but it's working, you need to change the adapter to bun adapter though!)

---
