#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *
print("starting..")
cpu = CPU()

cpu.load()
cpu.run()