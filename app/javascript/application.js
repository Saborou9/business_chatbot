// Configure your import map in config/importmap.rb
import "@hotwired/turbo-rails"
import "controllers"

// Add this to ensure Stimulus is properly initialized
import { application } from "controllers/application"

// Eager load all controllers
import { eagerLoadControllersFrom } from "@hotwired/stimulus-loading"
eagerLoadControllersFrom("controllers", application)
