import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["modal"]

  initialize() {
    console.log("ModalController initialized")
  }

  connect() {
    console.log("ModalController connected to element:", this.element)
    console.log("Data attributes:", this.element.dataset)
    this.modal = document.getElementById("new-chat-modal")
    console.log("Found modal element:", this.modal)
  }

  open(e) {
    console.log("Button clicked - opening modal")
    e.preventDefault()
    const modal = document.getElementById("new-chat-modal")
    console.log("Modal element at open time:", modal)
    if (modal) {
      modal.classList.remove("hidden")
      document.body.classList.add("overflow-hidden")
    }
  }
}
