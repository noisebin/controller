"""
multi.py, uses the sounddevice library to play multiple audio files to multiple output devices at the same time
Written by Devon Bray (dev@esologic.com)
"""
 
import sounddevice
import soundfile
import threading
import os
 
class Player:
    DATA_TYPE = "float32"

    def __init__(self, sounds_base_path):
        self.sound_base_paths = sounds_base_path
        self.sound_file_paths =  [
            path for path in sorted(filter(lambda path: self.good_filepath(path), self.sounds_base_path))
        ]
        print("Discovered the following .wav files:", self.sound_file_paths)
        self.files = [self.load_sound_file_into_memory(path) for path in self.sound_file_paths]
        self.streams = self.create_streams()

    def load_sound_file_into_memory(self, path):
        """
        Get the in-memory version of a given path to a wav file
        :param path: wav file to be loaded
        :return: audio_data, a 2D numpy array
        """

        audio_data, _ = soundfile.read(path, dtype=DATA_TYPE)
        return audio_data


    def get_device_number_if_usb_soundcard(self, index_info):
        """
        Given a device dict, return True if the device is one of our USB sound cards and False if otherwise
        :param index_info: a device info dict from PyAudio.
        :return: True if usb sound card, False if otherwise
        """

        index, info = index_info

        if "USB Audio Device" in info["name"]:
            return index
        return False


    def play_wav_on_index(self, audio_data, stream_object):
        """
        Play an audio file given as the result of `load_sound_file_into_memory`
        :param audio_data: A two-dimensional NumPy array
        :param stream_object: a sounddevice.OutputStream object that will immediately start playing any data written to it.
        :return: None, returns when the data has all been consumed
        """

        stream_object.write(audio_data)


    def create_running_output_stream(self, index):
        """
        Create an sounddevice.OutputStream that writes to the device specified by index that is ready to be written to.
        You can immediately call `write` on this object with data and it will play on the device.
        :param index: the device index of the audio device to write to
        :return: a started sounddevice.OutputStream object ready to be written to
        """

        output = sounddevice.OutputStream(
            device=index,
            dtype=DATA_TYPE
        )
        output.start()
        return output



    def good_filepath(self, path):
        """
        Macro for returning false if the file is not a non-hidden wav file
        :param path: path to the file
        :return: true if a non-hidden wav, false if not a wav or hidden
        """
        return str(path).endswith(".wav") and (not str(path).startswith("."))


    def create_streams(self):
        print("Files loaded into memory, Looking for USB devices.")
        usb_sound_card_indices = list(filter(lambda x: x is not False,
                                            map(self.get_device_number_if_usb_soundcard(),
                                                [index_info for index_info in enumerate(sounddevice.query_devices())])))
        print("Discovered the following usb sound devices", usb_sound_card_indices)
        return [self.create_running_output_stream(index) for index in usb_sound_card_indices]

    def play(self):
        running = True

        if not len(streams) > 0:
            running = False
            print("No audio devices found, stopping")

        if not len(files) > 0:
            running = False
            print("No sound files found, stopping")

        if running:
            print("Playing files")

            threads = [threading.Thread(target=play_wav_on_index, args=[file_path, stream])
                    for file_path, stream in zip(files, streams)]

            try:

                for thread in threads:
                    thread.start()

                for thread, device_index in zip(threads, usb_sound_card_indices):
                    print("Waiting for device", device_index, "to finish")
                    thread.join()

            except KeyboardInterrupt:
                running = False
                print("Stopping stream")
                for stream in streams:
                    stream.abort(ignore_errors=True)
                    stream.close()
                print("Streams stopped")

        print("Bye.")
