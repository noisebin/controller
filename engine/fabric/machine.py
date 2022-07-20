# import sys, signal
import os
import platform
from fabric.logging import Logger
# from fabric.configuration import Configuration
# from fabric.device_switch import Switch  # must come first, due to pin factory initialiser
# from fabric.device_ultrasonic import Ultrasonic

# import zmq
import ipaddress
from subprocess import check_output
# from datetime import datetime
# from time import sleep
# from dotmap import DotMap
#
# from inspect import ismethod, getmembers
from pprint import pprint, pformat

class Machine():

    device = None
    hardware = None
    os = None
    net_interface = None
    net_address = None
    net_status = None

    def __init__(self):
        # The Machine object is principally a metadata object that
        # detects and describes the core computer hardware running this system
        #
        # Gathering these concerns into a separate class isolates the
        # majority of the code from machine specific data and behaviours,
        # allowing it to run unchanged on a Mac laptop, Raspberry Pi
        # or anything else we haven't tried yet.
        #
        # Getting the whole controller to work on new hardware should
        # only require cloning/adapting the methods and constants in this module

        log = Logger()

        # Guess my hardware, OS and weight :)
        # posix.uname_result(sysname='Darwin', nodename='Pro.fritz.box', release='21.5.0', version='Darwin Kernel Version 21.5.0: Tue Apr 26 21:08:22 PDT 2022; root:xnu-8020.121.3~4/RELEASE_X86_64', machine='x86_64')
        # posix.uname_result(sysname='Linux', nodename='rpi', release='5.13.0-1031-raspi', version='#34-Ubuntu SMP PREEMPT Thu Jun 2 00:58:22 UTC 2022', machine='aarch64')

        self.os = str(os.uname())

        hw_cmd=None
        log.debug(f'Platform.system: {platform.system()}  platform.machine: {platform.machine()}')

        # Are we on a Mac Pro?
        if ((platform.system() == 'Darwin') and (platform.machine() == 'x86_64')):
            self.device = 'Mac'
            hw_cmd="system_profiler SPHardwareDataType |awk '/Model Name/ { sub(/^ +Model Name: /,\"\"); print }'"

        elif ((platform.system() == 'Linux') and (platform.machine() == 'aarch64')):
            self.device = 'RPi'
            hw_cmd='cat /proc/cpuinfo |grep Model |cut -f2 -d":" |cut -c2-'

        if (not self.device):
            log.debug('Unable to identify hardware platform - bailing out.')
            exit()

        try:
            self.hardware = check_output(hw_cmd, shell=True).decode()
        except CalledProcessError as e:
            log.warn(f'Hardware detection: Boooioioing!! {e}')
            exit()

        if (self.device == 'RPi'):
            self.net_interface = 'eth0'
            addr_cmd ='ip -br addr show dev eth0 |cut -f1 -d"/" |tr -s "\t "'
            try:
                result,self.net_status,self.net_address = check_output(addr_cmd, shell=True).decode().split()
                # eth0 UP 192.168.3.3
            except CalledProcessError as e:
                log.warn(f'Network address detection: Boooioioing!! {e}')
                exit()

        if (self.device == 'Mac'):
            self.net_interface = 'en0'
            addr_cmd ='ifconfig en0 |awk "/inet / { print \\"Address:\\" \$2 }; /status/ { sub(/^\tstatus: /,\\"Status:\\"); print }"'
            try:
                addr_result = check_output(addr_cmd, shell=True).decode().split()
                # ['Address:192.168.178.78', 'Status:active']

                self.net_address = addr_result[0].split(':')[1]
                self.net_status = addr_result[1].split(':')[1]
            except CalledProcessError as e:
                log.warn(f'Network address detection: Boooioioing!! {e}')
                exit()

        if (self.net_status not in ['active', 'inactive']):
            log.warn(f'net_status \'{pformat(self.net_status)}\' not recognised - bailing')
            exit()

        try:
            result = ipaddress.ip_address(self.net_address)
            log.debug(f'{self.net_interface} IP Address {self.net_address} syntactically valid, state is {self.net_status}')
        except ValueError:
            log.warn(f'{self.net_interface} has invalid IP address {self.net_address}')


    # @classmethod
    # def enqueue(cls, message):  # can access class (Ccls) attributes
