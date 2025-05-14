Rails.application.routes.draw do
  resources :messages
  devise_for :users,
    sign_out_via: [ :get, :delete ],
    controllers: {
      registrations: "registrations"
    }
  resources :chats, except: [ :edit, :update ] do
    resources :messages, only: [:create]
    member do
      patch :update_preferred_model
    end
  end

  get "/about", to: "pages#about", as: :about
  get "/pricing", to: "pages#pricing", as: :pricing

  # redirect /features to the home page’s #features section
  get "/features", to: redirect("/#features")

  # Chat health-check
  get "up" => "rails/health#show", as: :rails_health_check

  root "pages#home"
end
