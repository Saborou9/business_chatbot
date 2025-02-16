from fastapi import FastAPI, HTTPException
import subprocess
from bot_flow.src.bot_flow.main import BuddyFlow
import os
from datetime import datetime

app = FastAPI()

@app.post("/run_agent/")
async def run_agent(data: dict):
    user_input = data.get("input", "")
    
    if not user_input:
        raise HTTPException(status_code=400, detail="No input provided")

    # Generate a unique directory name based on current timestamp
    timestamp = datetime.now().strftime("%y_%m_%d_%H_%M_%S")
    directory = f"{timestamp}"
    os.makedirs(directory, exist_ok=True)

    try:
        flow_result = BuddyFlow(
            question=user_input,
            directory=directory,
            show_logs=False,
            model_name="sonnet",
            search_timeframe="d",
            search_results=10,
            search_results_parsed=2,
        ).kickoff()

        # Assuming the flow returns a response that can be extracted
        response = flow_result.final_response if hasattr(flow_result, 'final_response') else "No response generated"

        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
