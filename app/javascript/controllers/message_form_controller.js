import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["input", "submit"]

  connect() {
    this.element.addEventListener("turbo:submit-start", this.disableForm.bind(this))
    this.element.addEventListener("turbo:submit-end", this.enableForm.bind(this))
  }

  disableForm() {
    this.submitTarget.disabled = true
  }

  enableForm() {
    this.submitTarget.disabled = false
  }

  resetForm() {
    this.inputTarget.value = ""
    this.submitTarget.disabled = false
  }
}
