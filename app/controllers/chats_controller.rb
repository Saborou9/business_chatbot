class ChatsController < ApplicationController
  before_action :authenticate_user!
  before_action :set_chat, only: %i[ show destroy update_preferred_model ]

  # GET /chats or /chats.json
  def index
    @chats = current_user.chats
  end

  # GET /chats/1 or /chats/1.json
  def show
    @chats = current_user.chats
    respond_to do |format|
      format.html { render :show }
      format.turbo_stream
    end
  end

  # GET /chats/new
  def new
    @chat = current_user.chats.new
  end

  # POST /chats or /chats.json
  def create
    @chat = current_user.chats.new(chat_params)

    respond_to do |format|
      if @chat.save
        format.html { redirect_to @chat, notice: "Chat was successfully created." }
        format.json { render :show, status: :created, location: @chat }
      else
        format.html { render :new, status: :unprocessable_entity }
        format.json { render json: @chat.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /chats/1 or /chats/1.json
  def destroy
    @chat.destroy!

    respond_to do |format|
      format.html { redirect_to chats_path, status: :see_other, notice: "Chat was successfully destroyed." }
      format.json { head :no_content }
    end
  end

  def update_preferred_model
    Rails.logger.debug "Received params: #{params.inspect}"

    if @chat.update(params.require(:chat).permit(:preferred_model))
      respond_to do |format|
        format.turbo_stream { render turbo_stream: turbo_stream.replace("chat_content", partial: "chats/chat_content", locals: { chat: @chat }) }
        format.html { redirect_to chat_path(@chat), notice: "Model updated." }
      end
    else
      Rails.logger.error "Failed to update model: #{@chat.errors.full_messages.join(', ')}"

      respond_to do |format|
        format.turbo_stream { render turbo_stream: turbo_stream.replace("chat_content", partial: "chats/chat_content", locals: { chat: @chat }) }
        format.html { redirect_to chat_path(@chat), alert: "Failed to update model." }
      end
    end
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_chat
      @chat = current_user.chats.find(params.require(:id))
    end

    # Only allow a list of trusted parameters through.
    def chat_params
      params.require(:chat).permit(:title, :preferred_model)
    end
end
