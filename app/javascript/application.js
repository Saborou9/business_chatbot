// Configure your import map in config/importmap.rb
import "@hotwired/turbo-rails"
import "controllers"

// Eager load all controllers
import { eagerLoadControllersFrom } from "@hotwired/stimulus-loading"
eagerLoadControllersFrom("controllers", application)
