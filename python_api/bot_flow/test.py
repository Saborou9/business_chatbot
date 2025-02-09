from bot_flow.src.bot_flow.main import BuddyFlow

inputs = {
    
}

BuddyFlow(
    directory="10_2025_01_23_21_10_54",
    show_logs=False,
    model_name="4o-mini",
    search_timeframe="d",
    search_results=10,
    search_results_parsed=2,
).kickoff()