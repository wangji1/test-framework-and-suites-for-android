#!/usr/bin/env python
"""
Copyright (C) 2018 Intel Corporation
?
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
?
http://www.apache.org/licenses/LICENSE-2.0
?
Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions
and limitations under the License.
?

SPDX-License-Identifier: Apache-2.0
"""

# imports
import os
import sys
import time
from testlib.base.base_utils import get_args
from testlib.scripts.android.adb import adb_steps
from testlib.scripts.android.fastboot import fastboot_steps
from testlib.scripts.android.fastboot import fastboot_utils
from testlib.scripts.relay import relay_steps

# initialization
globals().update(vars(get_args(sys.argv)))
args = {}
for entry in script_args:  # noqa
    key, val = entry.split("=")
    args[key] = val
relay_type = args["relay_type"]
relay_port = args["relay_port"]
power_port = args["power_port"]

# test start
try:
    fastboot_utils.push_uiautomator_jar(serial=serial)  # noqa
    fastboot_steps.config_first_boot_wizard(serial=serial)()  # noqa

    os.system("mkdir -p ./temp/files/flash")
    fastboot_utils.creat_big_file("./temp/files/temp.txt", 0.1)
    adb_steps.connect_device(serial=serial)()  # noqa
    adb_steps.root_connect_device(serial=serial)()  # noqa
    time.sleep(5)
    os.system("adb push ./temp/files/temp.txt /data")

    fastboot_steps.factory_data_reset(serial=serial)()  # noqa
    adb_steps.connect_device(serial=serial)()  # noqa
    adb_steps.root_connect_device(serial=serial)()  # noqa
    time.sleep(5)
    file_exists = fastboot_utils.adb_command_file_or_directory_exists(
        name="temp.txt", command="adb shell ls /data")
    if file_exists:
        raise Exception("The test result did not achieve the desired results")

    os.system("sudo rm -rf ./temp")

except:
    relay_steps.reboot_main_os(serial=serial, relay_type=relay_type,  # noqa
                               relay_port=relay_port, power_port=power_port,
                               wait_ui=False, timeout=300, delay_power_on=30,
                               device_info="broxtonp", force_reboot=True)()
    fastboot_steps.factory_data_reset(serial=serial)()  # noqa
    os.system("sudo rm -rf ./temp")
    raise
# test end
