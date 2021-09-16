"""
multi.py, uses the sounddevice library to play multiple audio files to multiple output devices at the same time
Written by Devon Bray (dev@esologic.com), adapted by Ethan Crawford
"""

# The import command makes separate packages of code available to use in your program
# Here we are importing some packages that give us the ability to do extra things
import sounddevice # sounddevice lets us talk to the sound cards attached to the computer
import soundfile # soundfile lets us work with audio files
import threading # threading lets us tell the program to run more than one piece of code at the same time
import os # os gives us access to helpful Operating System commands
import time # time lets us do things with amounts of time
import random # random lets us do things like pick random numbers or make things happen randomly

# A class is another kind of self-contained package of code.
# It's like a template, and you can make a 'real object' (or even many of them) out of the same template.
# The class often has functions that other pieces of code can ask to do things.
# Here, the Player class is a package of code designed to handle playing sound samples from a
# folder of sounds on the computer.
class Player:
    # The kind of data that the samples are stored as
    # In this case, a special type of number, a 32 bit float number,
    # which allows us to store very large or very small numbers.
    DATA_TYPE = "float32"

    # __init__ is a special function that is automatically called when
    # we make a variable that holds an object made from the class
    # (like this: my_player = Player())
    # When an object made from the class is created like this,
    # we can give it some data as it is being created so that it can do things with this data.
    # (Here, as an object of the Player class is created, we expect to give it a bit of text that
    # points towards the folder of sounds that we want the player to choose sounds from to play.
    # We're calling this piece of text 'sounds_base_path' because it represents the base location
    # for the sounds we want the player to use).
    def __init__(self, sounds_base_path):
        # self is the object that we're creating - the player made from the Player class.
        # here, we make some variables to store bits of data that the player can use later -
        # (we're taking the base sounds location that we give the Player class when we create an object from it, and
        # storing it in a variable that is internally attached to *this* player we're creating)
        self.sounds_base_path = sounds_base_path
        # We also make a variable attached to this player we're creating that stores in a list all the paths
        # to each individual sound file that it finds at the base sounds location
        self.sound_file_paths = [
            os.path.join(self.sounds_base_path, path) for path in sorted(
                filter(
                    lambda path: self.good_filepath(path),
                    os.listdir(self.sounds_base_path)
                )
            )
        ]
        # Display a message printing out all the names and locations of the sound files we found
        print("Discovered the following .wav files:", self.sound_file_paths)

        # Read the contents of the sound files on the hard drive and load them into memory
        # (This code basically says, for each item in the sound_file_paths list, name it 'path',
        # and give this path to the load_sound_file_into_memory function. After each path is passed along this way,
        # Store all of the results in a variable which is a list called files).
        self.files = [self.load_sound_file_into_memory(path) for path in self.sound_file_paths]
        # Set up a variable (which starts as an empty list) to identify the sound cards attached to the computer
        # by number (eg a list such as [1, 2] where 1 and 2 are the first and second sound cards detected)
        self.usb_sound_card_indices = []
        # Set up a variable to hold some 'streams' of sound data that are sent to the sound cards to play
        self.streams = self.create_streams()
        # running_indices is a temporary bit of code to identify which sound streams are busy sending sound data
        # to the sound cards, or otherwise waiting for more sound data
        self.running_indices = [x for x in range(len(self.usb_sound_card_indices))]
        # Set up a variable to hold the state of each sound stream (running or not running - True or False).
        # This is a list, such as [False, False] where there are eg two streams and both are not currently running.
        # We mark each stream as not running (False) in the beginning because the player will start out silent
        # until the Ultrasound sensor detects something
        self.running = [False] * len(self.streams)
        # Set up a variable to track whether the player is allowed to make sound at all - starting out True
        # because we expect that the player will not be busy to begin with and should be allowed to play.
        self.can_run = True

    # The load_sound_file_into_memory function finds a sound file on the hard drive at the place that 'path' points to
    # and loads the contents of the sound file into memory
    def load_sound_file_into_memory(self, path):
        audio_data, _ = soundfile.read(path, dtype=self.DATA_TYPE)
        return audio_data

    # The get_device_number_if_usb_soundcard function will return the number that represents a soundcard
    # if it is a usb soundcard.
    # If it is not a usb souncard, the function returns false.
    # The index_info variable holds information that tells us about the soundcard.
    def get_device_number_if_usb_soundcard(self, index_info):
        # get the number (index) which points to this soundcard, and the info about this soundcard, from index_info
        index, info = index_info 
        if "USB Audio Device" in info["name"]:
            return index
        return False

    # The play_wav_on_index function plays sound data from the sound file
    # By sending it to the stream set up for the sound.
    # We pass into the function the following:
    # audio_data: the actual sound data to play
    # stream_object: the stream to make the sound flow through, into the sound card
    # running: the list that tracks whether each stream is currently busy (running) or not
    # index: the number that points towards which stream in the 'running' list we're going to use.
    def play_wav_on_index(self, audio_data, stream_object, running, index):
        try:
            # While the sound is playing on the stream, we want to tell the rest of the code
            # that the stream is busy (running) by setting one of the slots in the 'running' list to True.
            running[index] = True
            # Send the sound data into the stream
            stream_object.write(audio_data)
            # As soon as the sound has finished playing on the stream, we set the same slot in the 'running' list to False
            # So that the rest of the code knows that that stream is not busy (running) any more.
            running[index] = False
        except ValueError:
            # Sometimes, the code is unable to play a sound because it can't understand the sound's format.
            # In this case, it causes an error.
            # the 'except' above stops this error from crashing the program, and here we shuffle the list of sounds
            # so that next time a sound is picked to play, it is (hopefully) not the same broken one.
            running[index] = False
            random.shuffle(self.files)

    # The create_running_output_stream function creates a 'stream' for the sound data to flow through, into the sound card.
    # Here, index is the number pointing to the sound card that we want the stream to play into
    def create_running_output_stream(self, index):
        output = sounddevice.OutputStream(
            device=index,
            dtype=self.DATA_TYPE
        )
        output.start()
        return output


    # The good_filepath function is passed the path to a sound file, and returns True or False depending on whether
    # the sound file is playable by our system
    def good_filepath(self, path):
        # Return True if the file is a non-hidden wav file on the computer's hard drive,
        # Or return False if the file is not a wav or is hidden
        return str(path).endswith(".wav") and (not str(path).startswith("."))

    # The create_streams function creates a 'stream' for the sound data to flow through, into the sound card, for every
    # usb sound card that is detected by the computer.
    def create_streams(self):
        print("Files loaded into memory, Looking for USB devices.")
        # The following code basically says:
        # Create a list, and place into this list,
        # the numbers representing every sound device detected by the sounddevice package,
        # *where these devices are found to be usb sound cards*.
        # Then store this list in a variable in our player called 'usb_sound_card_indices'.
        self.usb_sound_card_indices = list(filter(lambda x: x is not False,
                                            map(self.get_device_number_if_usb_soundcard,
                                                [index_info for index_info in enumerate(sounddevice.query_devices())])))
        print("Discovered the following usb sound devices", self.usb_sound_card_indices)

        # Lastly, for each number of these usb sound card numbers, create a stream identified by the sound card's number,
        # and return the whole list of streams.
        return [self.create_running_output_stream(index) for index in self.usb_sound_card_indices]

    # The play function is where the player picks a sound to play, and plays it if there is an available sound device
    # that is not currently busy.
    def play(self):
        try:
            # make the can_run variable hold False or True depending on whether we find
            # every slot of the 'running' list to be True or False
            # (eg are all streams currently busy (running)? Then we *can't* play - set can_run to False.
            # are all streams currently empty (not running)? Then we *can* play - set can_run to True.
            self.can_run = all(val is False for val in self.running)
            # If we're able to play new sounds, then try to do so.
            if self.can_run is True:
                # if no streams were able to be created, we can't play.
                if not len(self.streams) > 0:
                    self.can_run = False
                    print("No audio devices found, stopping")

                # if no sound files were found, we can't play.
                if not len(self.files) > 0:
                    self.can_run = False
                    print("No sound files found, stopping")

                # if we *can* play,
                if self.can_run is True:
                    # pick a random sound file from the selection
                    random.shuffle(self.files)
                    print("Playing file: ?????????????")

                    # Create a 'thread' for each sound that is going to play.
                    # Threads are things that let us run more than one bit of code at the same time.
                    # The number of sounds that will play is limited by the number of sound cards.
                    # sound cards can play one sound at a time, so for two sound cards we can play two sounds at once.
                    # This means that we can play multiple sounds at the same time, as many as there are sound cards.
                    # Here, we create each thread and pass each one the name of the code function to run,
                    # and what pieces of data we need to give to the function (args).
                    # This means that each thread will run the play_wav_on_index function, but give it different args,
                    # including different sound file paths.
                    threads = [threading.Thread(target=self.play_wav_on_index, args=[file_path, stream, self.running, running_index])
                               for file_path, stream, running_index in zip(self.files, self.streams, self.running_indices)]

                    # Actually tell all the threads to start working
                    for thread in threads:
                        thread.start()

                    # Since we've just told the threads to start playing something,
                    # we don't want anything new to start playing until this lot has finished.
                    # Therefore, set the can_run variable to False until we are ready to play new sounds later
                    self.can_run = False
            else:
                # We tried to play new sounds while the current ones were still playing, so print a message
                print("All sound devices busy...")
        # If we stop the player playing by hitting the right keys on the keyboard to close the program,
        except KeyboardInterrupt:
            self.can_run = False
            print("Stopping stream")
            # Tidy up by Stopping and closing all the audio streams into the sound cards
            for stream in self.streams:
                stream.abort(ignore_errors=True)
                stream.close()
            print("Streams stopped")

            print("Bye.")
