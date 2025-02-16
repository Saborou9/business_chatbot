class Message < ApplicationRecord
  belongs_to :chat
  belongs_to :user

  validates :context, 
    presence: true, 
    length: { 
      minimum: 1, 
      maximum: 1000, 
      message: "must be between 1 and 1000 characters" 
    }

  validates :chat_id, :user_id, presence: true

  attribute :context, :string

  # Optional: Add a scope for recent messages
  scope :recent, -> { order(created_at: :desc).limit(50) }
end
