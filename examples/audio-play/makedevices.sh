#!/bin/bash

# create vitual sinks
pactl load-module module-null-sink sink_name=chan1 object.linger=1 media.class=Audio/Sink channel_map=FL
pactl load-module module-null-sink sink_name=chan2 object.linger=1 media.class=Audio/Sink channel_map=FL
pactl load-module module-null-sink sink_name=chan3 object.linger=1 media.class=Audio/Sink channel_map=FL
pactl load-module module-null-sink sink_name=chan4 object.linger=1 media.class=Audio/Sink channel_map=FL

# map real channels to virtual ones
pw-link chan1:monitor_1 alsa_output.usb-Plugable_Plugable_USB_Audio_Device_000000000000-00.analog-stereo:playback_FL
pw-link chan2:monitor_1 alsa_output.usb-Plugable_Plugable_USB_Audio_Device_000000000000-00.analog-stereo:playback_FR
pw-link chan3:monitor_1 alsa_output.usb-Plugable_Plugable_USB_Audio_Device_000000000000-00.2.analog-stereo:playback_FL
pw-link chan4:monitor_1 alsa_output.usb-Plugable_Plugable_USB_Audio_Device_000000000000-00.2.analog-stereo:playback_FR
