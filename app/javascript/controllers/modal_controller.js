import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  connect() {
    this.modal = this.element
    this.modal.classList.add("hidden") // Ensure modal starts hidden
  }

  open(e) {
    e.preventDefault()
    this.modal.classList.remove("hidden")
    document.body.classList.add("overflow-hidden")
  }

  close(e) {
    if (e) e.preventDefault()
    this.modal.classList.add("hidden")
    document.body.classList.remove("overflow-hidden")
  }
}
