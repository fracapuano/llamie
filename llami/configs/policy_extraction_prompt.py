POLICIES = {
    "grab_cup": {
        "description": "Can grab cups from the table"
    },
    "grab_pills": {
        "description": "Can grab medicine boxes from the table"
    },
    "grab_pen": {
        "description": "Can grab pens from the table"
    },
    "grab_banana": {
        "description": "Can grab bananas from the table"
    }
}

def get_extraction_prompt(user_input):
    policies_str = "\n".join([f"- {name}: {details['description']}" 
                             for name, details in POLICIES.items()])
    
    EXTRACTION_PROMPT = f"""Given the following list of available robot policies and their descriptions:
{policies_str}

Based on the user's request: {user_input}
Return ONLY the name of the most appropriate policy from the list. If none match well, return "none".
Response should be just the policy name or "none", nothing else."""
    
    return EXTRACTION_PROMPT