class AddApiKeysToUser < ActiveRecord::Migration[8.0]
  def change
    add_column :users, :openai_api_key, :string
    add_column :users, :deepseek_api_key, :string
    add_column :users, :anthropic_api_key, :string
  end
end
