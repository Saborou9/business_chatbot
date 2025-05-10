import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["modal", "form", "titleInput"]

  connect() {
    this.modal = document.getElementById("new-chat-modal")
  }

  open() {
    this.modal.classList.remove("hidden")
    document.body.classList.add("overflow-hidden")
    this.titleInputTarget?.focus()
  }

  close() {
    this.modal.classList.add("hidden")
    document.body.classList.remove("overflow-hidden")
    this.formTarget?.reset()
  }

  handleSubmit(e) {
    e.preventDefault()
    if (!this.titleInputTarget.value.trim()) {
      alert("Please enter a chat name")
      return
    }
    
    // Submit form via Turbo
    this.formTarget.requestSubmit()
  }
}
