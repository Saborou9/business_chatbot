import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["modal"]

  connect() {
    this.modal = document.getElementById("new-chat-modal")
  }

  open(e) {
    e.preventDefault()
    const modal = document.getElementById("new-chat-modal")
    if (modal) {
      modal.classList.remove("hidden")
      document.body.classList.add("overflow-hidden")
    }
  }

  close(e) {
    if (e) e.preventDefault();
    const modal = document.getElementById("new-chat-modal");
    if (modal) {
      modal.classList.add("hidden");
      document.body.classList.remove("overflow-hidden");
    }
  }

}
