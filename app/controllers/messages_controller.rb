require "net/http"
require "uri"
require "json"

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
        @bot_message = @chat.messages.new(
          context: bot_response,
          user: current_user,
          message_type: :bot
        )

        if @bot_message.save
          format.html { redirect_to chat_path(@chat), notice: "Messages created" }
          format.turbo_stream
        else
          puts "*" * 100
          puts @bot_message.errors.full_messages
          puts "*" * 100
          format.turbo_stream { render partial: "error" }
        end
      else
        format.turbo_stream { render partial: "error" }
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
    request = Net::HTTP::Post.new(uri.path, "Content-Type" => "application/json")
    request.body = {
      input: question,
      user_id: current_user.id,
      model_name: @chat.preferred_model || "gpt-3.5-turbo",
      api_keys: {
       openai: current_user.openai_api_key,
       deepseek: current_user.deepseek_api_key,
       anthropic: current_user.anthropic_api_key
     }
    }.to_json

    response = http.request(request)

    if response.code == "200"
      parsed_response = JSON.parse(response.body)
      parsed_response["response"]
    else
      "Sorry, I couldn't generate a response at this time."
    end
  rescue StandardError => e
    "An error occurred: #{e.message}"
  end
end
