class MessagesController < ApplicationController
  before_action :authenticate_user!
  before_action :set_chat

  def create
    @message = @chat.messages.new(message_params.merge(user: current_user))

    respond_to do |format|
      if @message.save
        # Trigger bot response generation here
        # This is a placeholder - you'll need to implement the actual bot response generation
        bot_response = generate_bot_response(@message)

        format.turbo_stream
        format.html { render partial: "messages/message", locals: { message: @message }, status: :ok }
      else
        format.turbo_stream { render turbo_stream: turbo_stream.replace("new_message", partial: "messages/form", locals: { chat: @chat, message: @message }) }
        format.html { render "chats/show", status: :unprocessable_entity }
      end
    end
  end

  private

  def set_chat
    @chat = current_user.chats.find(params[:chat_id])
  end

  def message_params
    params.require(:message).permit(:context)
  end

  def generate_bot_response(message)
    # Implement your bot response generation logic here
    # This is just a placeholder
    bot_response = @chat.messages.create(
      context: "This is a bot response to: #{message.context}",
      user: User.find_by(email: "bot@example.com")
    )
    bot_response
  end
end
