class RegistrationsController < Devise::RegistrationsController
  before_action :configure_permitted_parameters

  protected

  def sign_up_params
    params.require(:user).permit(:username, :email, :password, :password_confirmation)
  end

  def configure_permitted_parameters
    devise_parameter_sanitizer.permit(:sign_up, keys: [ :username ])
    devise_parameter_sanitizer.permit(:account_update, keys: [ :username ])
  end
end
