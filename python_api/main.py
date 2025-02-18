from fastapi import FastAPI, HTTPException
from bot_flow.src.bot_flow.main import BuddyFlow
import os
from datetime import datetime

app = FastAPI()

@app.post("/run_agent/")
async def run_agent(data: dict):
    user_input = data.get("input", "")
    user_id = data.get("user_id", "unknown")
    model_name = data.get("model_name", "4o-mini")
    
    if not user_input:
        raise HTTPException(status_code=400, detail="No input provided")

    # Create logs directory if it doesn't exist
    logs_base_dir = "logs"
    os.makedirs(logs_base_dir, exist_ok=True)

    # Generate a unique directory name based on user ID and current timestamp
    timestamp = datetime.now().strftime("%y_%m_%d_%H_%M_%S")
    directory = os.path.join(logs_base_dir, f"{user_id}_{timestamp}")
    os.makedirs(directory, exist_ok=True)

    try:
        flow = BuddyFlow(
            question=user_input,
            directory=directory,
            show_logs=False,
            model_name=model_name,
            search_timeframe="d",
            search_results=10,
            search_results_parsed=2,
        )

        flow_result = await flow.kickoff_async()

        # Assuming the flow returns a response that can be extracted
        response = flow_result.final_response if hasattr(flow_result, 'final_response') else "No response generated"

        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
