Rails.application.routes.draw do
  devise_for :users
  resources :chats, except: [ :edit, :update ]
  get "/about", to: "pages#about", as: :about
  get "/pricing", to: "pages#pricing", as: :pricing
  # Chat routes
  get "up" => "rails/health#show", as: :rails_health_check
  root "pages#home"
end
