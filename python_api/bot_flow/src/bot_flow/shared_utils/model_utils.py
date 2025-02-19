def get_model_api_key(model_name: str = 'gpt-4o-mini-2024-07-18', user_api_key: Optional[str] = None) -> str:
    """
    Maps model names to their corresponding API key environment variable names.
    
    :param model_name: The name of the AI model
    :return: The corresponding API key environment variable name
    """
    model_api_key_mapping = {
        'deepseek': ('DEEPSEEK_API_KEY', user_api_key),
        '4o-mini': ('OPENAI_API_KEY', user_api_key),
        '4o': ('OPENAI_API_KEY', user_api_key),
        'sonnet': ('ANTHROPIC_API_KEY', user_api_key),
        'haiku': ('ANTHROPIC_API_KEY', user_api_key)
    }
    
    # If model_name is a list, take the first element
    if isinstance(model_name, list):
        model_name = model_name[0] if model_name else 'gpt-4o-mini-2024-07-18'
    
    env_var_name, custom_key = model_api_key_mapping.get(model_name, ('OPENAI_API_KEY', None))

    if custom_key:
        return custom_key

    return env_var_name

def get_model_identifier(model_name: str = 'gpt-4o-mini-2024-07-18') -> str:
    """
    Translates full model names to shorter, more readable identifiers.
    
    :param model_name: The full name of the AI model
    :return: A shortened model identifier
    """
    model_identifier_mapping = {
        'deepseek': 'deepseek/deepseek-chat',
        '4o-mini': 'gpt-4o-mini-2024-07-18',
        '4o': 'gpt-4o-2024-11-20',
        'sonnet': 'claude-3-5-sonnet-20241022',
        'haiku': 'claude-3-5-haiku-20241022'
    }
    
    # If model_name is a list, take the first element
    if isinstance(model_name, list):
        model_name = model_name[0] if model_name else 'gpt-4o-mini-2024-07-18'
    
    return model_identifier_mapping.get(model_name, 'gpt-4o-mini-2024-07-18')
