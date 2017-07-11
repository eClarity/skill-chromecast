# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function

from adapt.intent import IntentBuilder

from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

import time
import pychromecast

__author__ = 'eClarity'

LOGGER = getLogger(__name__)

chromecasts = pychromecast.get_chromecasts()

class ChromecastSkill(MycroftSkill):
    def __init__(self):
        super(ChromecastSkill, self).__init__(name="ChromecastSkill")
        self.cc_device = self.config['cc_device']

    def initialize(self):
        cc_devices_intent = IntentBuilder("CCDevicesIntent"). \
            require("CCDevicesKeyword").build()
        self.register_intent(cc_devices_intent, self.handle_cc_devices_intent)

        cc_device_status_intent = IntentBuilder("CCDeviceStatusIntent"). \
            require("CCDeviceStatusKeyword").build()
        self.register_intent(cc_device_status_intent, self.handle_cc_device_status_intent)

        cc_muted_intent = IntentBuilder("CCMutedIntent"). \
            require("CCMutedKeyword").build()
        self.register_intent(cc_muted_intent, self.handle_cc_muted_intent)

        cc_play_media_intent = IntentBuilder("CCPlayMediaIntent"). \
            require("CCPlayMediaKeyword").build()
        self.register_intent(cc_play_media_intent, self.handle_cc_play_media_intent)

    def handle_cc_devices_intent(self, message):
        for cc in chromecasts:
            self.speak(cc.device.friendly_name)

    def handle_cc_device_status_intent(self, message):
        cc_device = self.cc_device
        cast = next(cc for cc in chromecasts if cc.device.friendly_name == cc_device)
        cast.wait()
        if cast.status.is_active_input == False:
            self.speak("Your Chromecast device is currently not active")
        elif cast.status.is_active_input == True:
            self.speak("Your Chromecast device is currently active")
        else:
            self.speak("Sorry I had trouble connecting to your chromecast")

    def handle_cc_muted_intent(self, message):
        cc_device = self.cc_device
        cast = next(cc for cc in chromecasts if cc.device.friendly_name == cc_device)
        cast.wait()
        if cast.status.volume_muted == False:
            self.speak("Your Chromecast device is currently not muted")
        elif cast.status.volume_muted == True:
            self.speak("Your Chromecast device is currently muted")
        else:
            self.speak("Sorry I had trouble connecting to your chromecast")

    def handle_cc_play_media_intent(self, message):
        cast = next(cc for cc in chromecasts if cc.device.friendly_name == cc_device)
        mc = cast.media_controller
        self.speak("Playing media on your chromecast now")
        mc.play_media('http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4', 'video/mp4')
        mc.block_until_active()

    def stop(self):
        pass


def create_skill():
    return ChromecastSkill()
