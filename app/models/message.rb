class Message < ApplicationRecord
  belongs_to :chat
  belongs_to :user

  validates :context, presence: true

  attribute :context, :string
end
