# Noisebin Web Console

A sub-project to provide a web interface to the controller engine.

The console will provide role-based access with:
  * a public view essentially showing status and history, and
  * an administrator view providing diagnostic level detail plus interactive control.

## Plausible Outline:
  * nginx serving a gateway written in Go, Ruby or PHP.  Ok, Node if we really have to.
  * Status sourced from the SQLite database, and ZeroMQ queues for events out, command input.
  * Front end based on Vue.js

The console will be able to operate locally in the Raspberry Pi's Ubuntu desktop if we are driving it from a direct-attached screen and keyboard, but will normally run remotely.
