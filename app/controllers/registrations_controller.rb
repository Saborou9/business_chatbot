class RegistrationsController < Devise::RegistrationsController
  before_action :configure_permitted_parameters

  protected

  def sign_up_params
    puts "Params received: #{params.inspect}"
    params.require(:user).permit(:username, :email, :password, :password_confirmation)
  end

  def configure_permitted_parameters
    devise_parameter_sanitizer.permit(:sign_up, keys: [ :username ])
    devise_parameter_sanitizer.permit(:account_update, keys: [ :username ])
  end

  def configure_permitted_parameters
    devise_parameter_sanitizer.permit(:sign_up, keys: [ :username, :openai_api_key, :deepseek_api_key, :anthropic_api_key ])
    devise_parameter_sanitizer.permit(:account_update, keys: [ :username, :openai_api_key, :deepseek_api_key, :anthropic_api_key ])
  end
end
