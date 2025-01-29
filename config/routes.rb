Rails.application.routes.draw do
  devise_for :users
  get "up" => "rails/health#show", as: :rails_health_check
  root "pages#home"
  get '/about', to: 'pages#about', as: :about
  get '/pricing', to: 'pages#pricing', as: :pricing
  get '/signup', to: 'pages#signup', as: :signup
  get '/login', to: 'pages#login', as: :login
  
  # Chat routes
  resources :chat, only: [:index, :create]
end
