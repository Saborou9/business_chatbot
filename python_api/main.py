from fastapi import FastAPI, HTTPException
from fastapi.concurrency import run_in_threadpool
from bot_flow.src.bot_flow.main import BuddyFlow
import os
from datetime import datetime
from typing import Dict, Any

app = FastAPI()

@app.post("/run_agent/")
async def run_agent(data: Dict[str, Any]):
    user_input = data.get("input", "")
    user_id = data.get("user_id", "unknown")
    model_name = data.get("model_name", "4o-mini")
    
    if not user_input:
        raise HTTPException(status_code=400, detail="No input provided")

    # Create logs directory
    logs_base_dir = "logs"
    os.makedirs(logs_base_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%y_%m_%d_%H_%M_%S")
    directory = os.path.join(logs_base_dir, f"{user_id}_{timestamp}")
    os.makedirs(directory, exist_ok=True)

    try:
        # Run synchronous BuddyFlow in threadpool
        flow_result = await run_in_threadpool(
            lambda: BuddyFlow(
                question=user_input,
                directory=directory,
                show_logs=True,
                model_name=model_name,
                search_timeframe="d",
                search_results=2,
                search_results_parsed=1,
            ).kickoff()
        )

        # Ensure we return a proper JSON response
        return {
            "status": "success",
            "response": flow_result,
            "timestamp": timestamp,
            "user_id": user_id
        }

    except Exception as e:
        error_detail = str(e)
        print(f"Error processing request: {error_detail}")  # Log the error
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": "Failed to process request",
                "error": error_detail
            }
        )
