class Message < ApplicationRecord
  belongs_to :chat
  belongs_to :user

  enum :message_type, [ :user, :bot ], prefix: true

  validates_presence_of :context, :chat_id, :user_id
  validates_length_of :context, minimum: 1, maximum: 1000, message: "must be between 1 and 1000 characters", if: -> { message_type_user? }

  # Optional: Add a scope for recent messages
  scope :recent, -> { order(created_at: :desc).limit(50) }
end
