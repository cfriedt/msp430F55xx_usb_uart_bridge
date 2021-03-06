# BSD 3-Clause License
# 
# Copyright (c) 2020, Erik Larson
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# echo_test.py
#
#  Created on: May 7, 2020
#      Author: Erik Larson
import serial
import argparse
import random

###############################################
# Assumed setup:
# USB CDC used for `port`
# UART on board wired for loopback
###############################################
parser = argparse.ArgumentParser(description='Test USB/UART bridge with random data')
parser.add_argument('port', help='serial port')
parser.add_argument('-t', '--tests', type=int, default=100, help='number of messages to send')
parser.add_argument('-m', '--max', type=int, default=5000, help='maximum message size')
parser.add_argument('-r', '--random', action='store_true', help='randomize data; default sequential')

args = parser.parse_args()
print(args.port, args.tests, args.max)

with serial.Serial(args.port, 115200, timeout=3, write_timeout=3) as ser:
    for i in range(args.tests):
        size = random.randint(1,args.max)
        payload = bytearray((random.getrandbits(8) if args.random else x%256) for x in range(size))
        ser.write(payload)
        response = ser.read(size)
        result = payload == response
        resultmsg = 'OK' if result else f"({len(response)} bytes received) [FAIL]"

        print(f"{i+1}: {size} byte message {resultmsg}")
        if not result:
            for k in range(size):
                if payload[k] != response[k]:
                    print(f"{k}: {hex(payload[k])} != {hex(response[k])}")
            break

