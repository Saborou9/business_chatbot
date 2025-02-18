class Chat < ApplicationRecord
  belongs_to :user
  has_many :messages, dependent: :destroy
  validates :title, presence: true

  validates :preferred_model,
    inclusion: {
      in: [ "deepseek", "4o-mini", "4o", "sonnet", "haiku" ],
      allow_nil: true
    }
end
