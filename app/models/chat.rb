class Chat < ApplicationRecord
  belongs_to :user
  has_many :messages, dependent: :destroy
  validates :title, presence: true

  validates :preferred_model,
    inclusion: {
      in: [ "GPT-3.5", "GPT-4", "Claude-2", "Gemini", "Anthropic" ],
      allow_nil: true
    }
end
