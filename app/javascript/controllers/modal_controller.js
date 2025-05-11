import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["modal", "form", "titleInput"]

  initialize() {
    console.debug("ModalController initialized")
  }

  connect() {
    console.debug("ModalController connected to element:", this.element)
    this.modal = this.modalTarget || this.element
    if (!this.modal) {
      console.error("ModalController: No modal element found!")
    }
  }

  open(e) {
    try {
      if (e) e.preventDefault()
      
      if (!this.modal) {
        console.error("ModalController: Cannot open - modal reference missing")
        return
      }

      console.debug("Opening modal")
      this.modal.classList.remove("hidden")
      document.body.classList.add("overflow-hidden")
      
      if (this.hasTitleInputTarget) {
        this.titleInputTarget.focus()
      }
    } catch (error) {
      console.error("ModalController open error:", error)
    }
  }

  close(e) {
    try {
      if (e) e.preventDefault()
      
      if (!this.modal) {
        console.error("ModalController: Cannot close - modal reference missing")
        return
      }

      console.debug("Closing modal")
      this.modal.classList.add("hidden")
      document.body.classList.remove("overflow-hidden")
      
      if (this.hasFormTarget) {
        this.formTarget.reset()
      }
    } catch (error) {
      console.error("ModalController close error:", error)
    }
  }

  handleSubmit(e) {
    try {
      if (!this.hasTitleInputTarget || !this.titleInputTarget.value.trim()) {
        e.preventDefault()
        alert("Please enter a chat name")
        if (this.hasTitleInputTarget) {
          this.titleInputTarget.focus()
        }
      }
    } catch (error) {
      console.error("ModalController submit error:", error)
    }
  }
}
