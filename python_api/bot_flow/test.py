from bot_flow.src.bot_flow.main import BuddyFlow

inputs = {
    'podcast_name': 'Legends of the Realm',
     'topic': 'The heroic tale of Sir Galahad and the quest for the Holy Grail',
     'search_results_parsed': 5,
     'podcast_title': 'Legends of the Realm',
     'word_count': 1000,
     'include_sponsor': False,
     'sponsor_segment': 'This episode is brought to you by Castle Forge, crafting authentic medieval experiences!',
     'sponsor_name': 'Castle Forge',
     'introduction': "Welcome to Legends of the Realm – where history, myth, and heroism intertwine. Each episode transports you to the age of chivalry, unraveling the most captivating stories of medieval knights and their extraordinary quests.",
     'afterword': "That's all for today's epic tale. Join us next time as we continue to explore the rich tapestry of medieval legends and the knights who shaped history.",
     'hosts': """
     - Sir Roland: A medieval historian with a passion for knightly lore and epic storytelling.
     - Lady Eleanora: A scholar of Arthurian legends and medieval culture.
     - Master Cedric: A storyteller and expert in medieval combat and chivalric codes.
     - Baroness Isabelle: A descendant of noble lineage with deep knowledge of medieval court life.
     """,
     'hosts_names': ['Roland', 'Eleanora', 'Cedric', 'Isabelle'],
}

StorytellingFlow(
    user_id=1,
    directory="10_2025_01_23_21_10_54",
    show_logs=False,
    podcast_name=inputs['podcast_name'],
    topic=inputs['topic'],
    word_count=inputs['word_count'],
    hosts=inputs['hosts'],
    hosts_names=inputs['hosts_names'],
    model_name="4o-mini",
    search_timeframe="d",
    search_results=10,
    search_results_parsed=2,
    style="narrative storytelling",
    story_type="narrative",
    number_of_characters=3,
    target_emotional_intensity="moderate",
    mood="neutral",
    setting_complexity="moderate",
).kickoff()