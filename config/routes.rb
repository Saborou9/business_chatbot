Rails.application.routes.draw do
  get "up" => "rails/health#show", as: :rails_health_check
  root "pages#home"
  get '/about', to: 'pages#about', as: :about
  get '/pricing', to: 'pages#pricing', as: :pricing
  get '/signup', to: 'pages#signup', as: :signup
end
