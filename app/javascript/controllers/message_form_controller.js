import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["input", "submit"]

  showLoading() {
    this.submitTarget.disabled = true
    // Show loading indicator
    document.getElementById('loading-indicator')?.classList.remove('hidden')
  }

  hideLoading() {
    this.submitTarget.disabled = false
    // Hide loading indicator
    document.getElementById('loading-indicator')?.classList.add('hidden')
    this.inputTarget.value = ""
  }
}
