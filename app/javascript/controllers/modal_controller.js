import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["modal", "form", "titleInput"]

  connect() {
    this.modal = document.getElementById("new-chat-modal")
    this.modal.classList.remove("hidden") // Keep modal visible by default
  }

  close() {
    if (this.modal) {
      this.modal.classList.add("hidden")
      document.body.classList.remove("overflow-hidden")
    }
  }

  validateAndSubmit(e) {
    if (!this.titleInputTarget.value.trim()) {
      e.preventDefault()
      alert("Please enter a chat name")
      this.titleInputTarget.focus()
    }
  }
}
