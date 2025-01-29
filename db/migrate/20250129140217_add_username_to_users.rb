class AddUsernameToUsers < ActiveRecord::Migration[8.0]
  def change
    # Add column only if it doesn't exist
    add_column :users, :username, :string, null: true unless column_exists?(:users, :username)
    
    # Add unique index only if it doesn't exist
    add_index :users, :username, unique: true unless index_exists?(:users, :username)
  end
end
