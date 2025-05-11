class ChatsController < ApplicationController
  before_action :authenticate_user!
  
  # GET /chats/new
  def new
    @chat = current_user.chats.new
    respond_to do |format|
      format.html # Renders new.html.erb
      format.turbo_stream # Renders new.turbo_stream.erb
    end
  end

  # POST /chats
  def create
    @chat = current_user.chats.new(chat_params)
    
    if @chat.save
      redirect_to @chat, notice: "Chat created successfully"
    else
      render :new, status: :unprocessable_entity
    end
  end

  private

  def chat_params
    params.require(:chat).permit(:title, :preferred_model)
  end
end
