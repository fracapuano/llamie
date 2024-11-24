import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
from llami.backend.robot_server import extract_policy
from llami.configs.policy_extraction_prompt import get_extraction_prompt
app = FastAPI()

def available_policies():
    """
    Return the list of available policies in configs/trained_policies
    """
    directory = "llami/configs/trained_policies/"
    return [f.name[:-5] for f in os.scandir(directory) if f.name.endswith(".yaml")]

def extract_policy(text: str):
    policies = available_policies()

    # Easy version supposing all policies are of the form "grab_object"
    objects = [policy.split("_")[1] for policy in policies]
    for ind, object in enumerate(objects):
        if object in text:
            return policies[ind]
    
    # Actually we should rerun Llama if no policy is found
    return policies[0]  # Default policy

# Define input schema
class LlamaRequest(BaseModel):
    prompt: str
# Define the endpoint

@app.post("/llama")
async def process_prompt(prompt_request: LlamaRequest):
    # Prepare the payload for the POST request
    
    prompt = get_extraction_prompt(prompt_request.prompt)
    payload = {
        "prompt": prompt,
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
