- The current code assumes that samples will all be playable as-is on the detected sound devices. This currently means that all samples need to be converted to a sample rate of 48k, as this is the only sample rate that the current USB sound devices accept.
- There is a problem where `multi.py` tries to play sounds on different USB audio devices, but eventually ends up refusing to do so because all of them end up being still 'in use'. I don't remember the exact details, but it might be in part to do with the convenience function `play`, provided by the Python `sounddevice` library, not being threadsafe. More investigation of the code is needed - particularly by looking at the various log messages produced as the code runs. It _may_ involve having to revert the use of `play` and go back to manually setting up our own `OutputStream`s.