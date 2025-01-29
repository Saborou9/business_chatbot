# frozen_string_literal: true

class DeviseCreateUsers < ActiveRecord::Migration[8.0]
  def change
    # Remove create_table block
    # Add or modify columns conditionally
    
    # Authenticatable
    change_table :users do |t|
      unless column_exists?(:users, :email)
        t.string :email, null: false, default: ""
      end
      
      unless column_exists?(:users, :encrypted_password)
        t.string :encrypted_password, null: false, default: ""
      end

      # Recoverable
      unless column_exists?(:users, :reset_password_token)
        t.string :reset_password_token
      end
      
      unless column_exists?(:users, :reset_password_sent_at)
        t.datetime :reset_password_sent_at
      end

      # Rememberable
      unless column_exists?(:users, :remember_created_at)
        t.datetime :remember_created_at
      end

      # Optional: Trackable
      unless column_exists?(:users, :sign_in_count)
        t.integer :sign_in_count, default: 0, null: false
      end
      
      unless column_exists?(:users, :current_sign_in_at)
        t.datetime :current_sign_in_at
      end
      
      unless column_exists?(:users, :last_sign_in_at)
        t.datetime :last_sign_in_at
      end
      
      unless column_exists?(:users, :current_sign_in_ip)
        t.string :current_sign_in_ip
      end
      
      unless column_exists?(:users, :last_sign_in_ip)
        t.string :last_sign_in_ip
      end
    end

    # Add indexes if they don't exist
    add_index :users, :email, unique: true unless index_exists?(:users, :email)
    add_index :users, :reset_password_token, unique: true unless index_exists?(:users, :reset_password_token)
  end
end
