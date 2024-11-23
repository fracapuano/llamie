from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
from llami.backend.robot_server import extract_policy

app = FastAPI()

# Define input schema
class PromptRequest(BaseModel):
    whisper_output: str

# Define the endpoint
@self.app.post("/llama")
async def process_prompt(prompt_request: PromptRequest):
    # Prepare the payload for the POST request
    
    payload = {
        "prompt": prompt_request.prompt,
        "n_predict": 128
    }
    
    # Target URL
    target_url = "http://localhost:8080/completion"
    
    try:
        # Make the POST request to the external API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url=target_url,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
        # Raise an exception if the request failed
        response.raise_for_status()

        # Parse the response JSON
        response_data = response.json()
        # Extract the `answer` key
        if "content" in response_data:

            policy = extract_policy(response_data["content"])

        
            fancesco_url = f"http://localhost:8080/execute_policy/{policy}"
            # Make the POST request to the external API
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url=target_url,
                    headers={"Content-Type": "application/json"}
                )
                
                
            return {"content": response_data["content"]}
        else:
            raise HTTPException(status_code=500, detail="Invalid response from external API")

    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {e}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"HTTP error: {e}")
