// Configure your import map in config/importmap.rb
import "@hotwired/turbo-rails"
import "controllers"

// Add this to ensure Stimulus is properly initialized
import { application } from "controllers/application"
import ModalController from "./controllers/modal_controller"

// Manually register the controller
application.register("modal", ModalController)

// Debug statement to verify registration
console.log("Registered controllers:", application.controllers)

// Eager load all controllers
import { eagerLoadControllersFrom } from "@hotwired/stimulus-loading"
eagerLoadControllersFrom("controllers", application)
