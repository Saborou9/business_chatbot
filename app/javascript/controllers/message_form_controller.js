import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["input", "submit"]

  connect() {
    // Automatically disable during submission and re-enable after
    this.element.addEventListener("turbo:submit-start", () => {
      this.submitTarget.disabled = true
    })
    this.element.addEventListener("turbo:submit-end", () => {
      this.submitTarget.disabled = false
    })
  }

  resetForm() {
    this.inputTarget.value = ""
    this.submitTarget.disabled = false
  }
}
