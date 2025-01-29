class ChatController < ApplicationController
  before_action :authenticate_user!

  def index
    # Fetch recent chat messages or initialize a new chat
    @messages = current_user.messages.order(created_at: :desc).limit(50)
  end

  def create
    # Create a new message
    @message = current_user.messages.build(message_params)

    if @message.save
      # Broadcast the message to the chat room
      ActionCable.server.broadcast "chat_channel", message: render_message(@message)
      head :ok
    else
      render json: { errors: @message.errors.full_messages }, status: :unprocessable_entity
    end
  end

  private

  def message_params
    params.require(:message).permit(:content)
  end

  def render_message(message)
    ApplicationController.renderer.render(partial: 'messages/message', locals: { message: message })
  end
end
