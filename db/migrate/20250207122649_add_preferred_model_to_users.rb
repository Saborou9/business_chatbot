class AddPreferredModelToUsers < ActiveRecord::Migration[8.0]
  def change
    add_column :users, :preferred_model, :string
  end
end
