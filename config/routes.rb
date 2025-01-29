Rails.application.routes.draw do
  devise_for :users, controllers: { 
    registrations: 'registrations',
    sessions: 'devise/sessions'
  }
  get "up" => "rails/health#show", as: :rails_health_check
  root "pages#home"
  get '/about', to: 'pages#about', as: :about
  get '/pricing', to: 'pages#pricing', as: :pricing
  # Chat routes
  resources :chat, only: [:index, :create]
end
