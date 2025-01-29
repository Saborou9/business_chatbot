class AddDeviseToUsers < ActiveRecord::Migration[8.0]
  def self.up
    change_table :users, bulk: true do |t|
      # Use if_not_exists: true for each column
      t.string :email, null: false, default: "", if_not_exists: true
      t.string :encrypted_password, null: false, default: "", if_not_exists: true
      t.string :reset_password_token, if_not_exists: true
      t.datetime :reset_password_sent_at, if_not_exists: true
      t.datetime :remember_created_at, if_not_exists: true
    end

    # Use safe_add_index with if_not_exists: true
    add_index :users, :email, unique: true, if_not_exists: true
    add_index :users, :reset_password_token, unique: true, if_not_exists: true
  end

  def self.down
    # Provide a safe way to rollback
    remove_index :users, :email if index_exists?(:users, :email)
    remove_index :users, :reset_password_token if index_exists?(:users, :reset_password_token)
    
    remove_columns :users, :email, :encrypted_password, :reset_password_token, :reset_password_sent_at, :remember_created_at
  end
end
