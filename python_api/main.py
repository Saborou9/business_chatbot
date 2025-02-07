from fastapi import FastAPI
import subprocess
from crewai import Crew

app = FastAPI()

app.post("/run_agent/")
async def run_agent(data: dict):
    user_input = data.get("input", "")
    
    result = subprocess.run(["python3", "agent.py", user_input], capture_output=True, text=True)

    return {"response": result.stdout.strip()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)