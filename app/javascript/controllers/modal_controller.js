import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["modal", "form", "titleInput"]

  connect() {
    this.modal = document.getElementById("new-chat-modal")
  }

  open(e) {
    e.preventDefault()
    this.modal.classList.remove("hidden")
    document.body.classList.add("overflow-hidden")
    this.titleInputTarget?.focus()
  }

  close(e) {
    if (e) e.preventDefault()
    this.modal.classList.add("hidden")
    document.body.classList.remove("overflow-hidden")
    this.formTarget?.reset()
  }

  handleSubmit(e) {
    if (!this.titleInputTarget.value.trim()) {
      e.preventDefault()
      alert("Please enter a chat name")
      this.titleInputTarget.focus()
    }
    // Let form submit normally if valid
  }
}
