class MessagesController < ApplicationController
  before_action :authenticate_user!
  before_action :set_chat

  def create
    @message = @chat.messages.new(message_params.merge(user: current_user))

    respond_to do |format|
      if @message.save
        format.turbo_stream
        format.html { redirect_to @chat }
      else
        format.turbo_stream { render turbo_stream: turbo_stream.replace(@message, partial: "messages/form", locals: { chat: @chat, message: @message }) }
        format.html { render 'chats/show', status: :unprocessable_entity }
      end
    end
  end

  private

  def set_chat
    @chat = current_user.chats.find(params[:chat_id])
  end

  def message_params
    params.require(:message).permit(:content)
  end
end
