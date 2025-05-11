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

  close(e) {
    if (e) e.preventDefault();
    const modal = document.getElementById("new-chat-modal");
    if (modal) {
      modal.classList.add("hidden");
      document.body.classList.remove("overflow-hidden");
    }
  }

  handleManualOpen() {
    this.connect(); // Force controller connection
    const modal = document.getElementById('new-chat-modal');
    if (modal) {
      modal.classList.remove('hidden');
      document.body.classList.add('overflow-hidden');
    }
  }
}

document.addEventListener('manual:open', () => {
  const controller = application.getControllerForElementAndIdentifier(
    document.getElementById('new-chat-modal'), 
    'modal'
  );
  controller?.handleManualOpen();
});
