import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["input", "submit"]

  showLoading() {
    this.submitTarget.disabled = true
    const loadingIndicator = document.getElementById('loading-indicator')
    if (loadingIndicator) {
      loadingIndicator.classList.remove('hidden')
    }
  }

  hideLoading() {
    this.submitTarget.disabled = false
    const loadingIndicator = document.getElementById('loading-indicator')
    if (loadingIndicator) {
      loadingIndicator.classList.add('hidden')
    }
    this.inputTarget.value = ""
  }
}
