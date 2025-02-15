from src.bot_flow.main import BuddyFlow

BuddyFlow(
    question="What are the biggest competitors in AI software market?",
    directory="10_2025_01_23_21_10_54",
    show_logs=False,
    model_name="sonnet",
    search_timeframe="d",
    search_results=10,
    search_results_parsed=2,
).kickoff()
