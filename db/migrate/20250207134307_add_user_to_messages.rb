class AddUserToMessages < ActiveRecord::Migration[8.0]
  def change
    add_reference :messages, :user, null: false, foreign_key: true
    add_column :messages, :context, :text
  end
end
