import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["modal"]

  connect() {
    // Find the modal element in the DOM
    this.modal = document.getElementById("new-chat-modal")
  }

  open() {
    if (this.modal) {
      this.modal.classList.remove("hidden")
      document.body.classList.add("overflow-hidden")
    }
  }

  close() {
    if (this.modal) {
      this.modal.classList.add("hidden")
      document.body.classList.remove("overflow-hidden")
    }
  }
}
