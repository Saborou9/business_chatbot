// Configure your import map in config/importmap.rb
import "@hotwired/turbo-rails"
import "controllers"

// Debug before registration
console.log("Registering modal controller...")

// Register controller
import { application } from "controllers/application"
import ModalController from "./controllers/modal_controller"
application.register("modal", ModalController)

// Debug after registration
console.log("Registered controllers:", Object.keys(application.controllers))

// Eager load all controllers
import { eagerLoadControllersFrom } from "@hotwired/stimulus-loading"
eagerLoadControllersFrom("controllers", application)
