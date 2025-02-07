class User < ApplicationRecord
  # Include default devise modules. Others available are:
  # :confirmable, :lockable, :timeoutable, :trackable and :omniauthable
  devise :database_authenticatable, :registerable,
         :recoverable, :rememberable, :validatable

  has_many :chats, dependent: :destroy
  has_many :messages, through: :chats

  # Username validations
  validates :username,
    presence: true,
    uniqueness: { case_sensitive: false },
    format: {
      with: /\A[a-zA-Z0-9_]+\z/,
      message: "can only contain letters, numbers, and underscores"
    },
    length: { minimum: 3, maximum: 20 }

  validates :preferred_model,
    inclusion: {
      in: [ "GPT-3.5", "GPT-4", "Claude-2", "Gemini", "Anthropic" ],
      allow_nil: true
    }
end
