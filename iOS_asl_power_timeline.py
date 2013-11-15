#!/usr/bin/env python3

"""
Copyright (c) 2012, CCL Forensics
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the CCL Forensics nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL CCL FORENSICS BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import sys
import os
import os.path as path
import re
import ccl_asldb

__version__ = "0.3.0"
__description__ = "Reads the ASL log files in the DiagnosticMessages folder on an iOS device and presents a timeline of battery charge as a csv file"
__contact__ = "Alex Caithness"
__outputtype__ = 0
__outputext__ = "csv"

"""
work_input - tuple containing the path to the DiagnosicMessage directory
work_output - tuple containing the path for the output csv file
"""

def __dowork__(work_input, work_output):
    # Unpack input
    if not isinstance(work_input, tuple) or len(work_input) < 1:
        raise ValueError("work_input must be a tuple containing the path for the input database")
    
    if not isinstance(work_output, tuple) or len(work_output) < 1:
        raise ValueError("work_output must be a tuple containing the path for the output html report")
    
    input_dir = work_input[0]
    output_file_path = work_output[0]

    # Going to write the power events and order them in memory. Should never be an issue, but if it is, here is where it needs to be fixed.
    power_events = []

    for file_path in os.listdir(input_dir):
        file_path = path.join(input_dir, file_path)
        print("Reading {0}".format(file_path))
        try:
            f = open(file_path, "rb")
        except IOError as e:
            print("Couldn't open file {0} ({1}). Skipping this file".format(file_path, e))
            continue

        try:
            db = ccl_asldb.AslDb(f)
        except ccl_asldb.AslDbError as e:
            print("Couldn't open file {0} ({1}). Skipping this file".format(file_path, e))
            f.close()
            continue

       
        for record in db:
            # Reasons to skip
            if record.sender != "powerd":
                continue
            if "com.apple.message.domain" not in record.key_value_dict:
                continue
            if record.key_value_dict["com.apple.message.domain"].lower() not in ("com.apple.powermanagement.sleep", "com.apple.powermanagement.wake"):
                continue

            # OK, we have a record we want, pull out the charge value using regular expressions (now I have two problems etc.)
            charge_match = re.search(r"\d{1,3}(?=%)", record.message)
            if not charge_match:
                print("An entry in {0} which looked legit didn't have a charge percentage, skipping...".format(file_path))
                continue
            power_source_match = re.search("(?<=Using )([A-z]+)", record.message)
            power_source = power_source_match.group(0) if power_source_match else ""

            power_events.append((record.timestamp, charge_match.group(0), power_source))

        f.close()

    # Sort and write out
    out = open(output_file_path, "w", encoding="utf-8")
    for charge_tuple in sorted(power_events, key=lambda x:x[0]):
        out.write("{0:%d/%m/%Y %H:%M:%S},{1},{2}\n".format(charge_tuple[0], charge_tuple[1], charge_tuple[2]))

    out.close()



def __main__():
    if len(sys.argv) < 2:
        print()
        print("Usage: {0} <DiagnosticMessages folder> <output>".format(os.path.basename(sys.argv[0])))
        print()
        sys.exit(1)
    else:
        work_input = (sys.argv[1],)
        work_output = (sys.argv[2],)
        __dowork__(work_input, work_output)

if __name__ == "__main__":
    __main__()