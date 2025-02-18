require 'net/http'
require 'uri'
require 'json'

class MessagesController < ApplicationController
  before_action :authenticate_user!
  before_action :set_chat

  def create
    @message = @chat.messages.new(message_params.merge(user: current_user))

    respond_to do |format|
      if @message.save
        # Send request to Python API
        bot_response = send_to_agent(@message.context)

        # Create bot message in the chat
        bot_message = @chat.messages.create(
          context: bot_response,
          user: User.find_by(email: 'bot@example.com')
        )

        format.turbo_stream
        format.html { render partial: 'messages/message', locals: { message: @message }, status: :ok }
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

  def send_to_agent(question)
    uri = URI.parse("http://localhost:8000/run_agent/")
    
    http = Net::HTTP.new(uri.host, uri.port)
    request = Net::HTTP::Post.new(uri.path, 'Content-Type' => 'application/json')
    request.body = { 
      input: question, 
      user_id: current_user.id 
    }.to_json

    response = http.request(request)
    
    if response.code == '200'
      parsed_response = JSON.parse(response.body)
      parsed_response['response']
    else
      "Sorry, I couldn't generate a response at this time."
    end
  rescue StandardError => e
    "An error occurred: #{e.message}"
  end
end
