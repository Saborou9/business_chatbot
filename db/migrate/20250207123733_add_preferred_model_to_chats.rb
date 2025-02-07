class AddPreferredModelToChats < ActiveRecord::Migration[8.0]
  def change
    add_column :chats, :preferred_model, :string
  end
end
