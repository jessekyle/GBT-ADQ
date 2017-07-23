#! /usr/bin/python

import subprocess
import os

BLC00 = subprocess.check_output("/home/jkyle/GBT-ADQ/mysql/blc/blc00")
#print(BLC00[0:5])
#print(BLC00[5:].strip("\n"))
print(BLC00[0:5].strip("\n") + ",host=" + BLC00[5:].strip("\n") + 
	",region=us value=1")
BLC01 = subprocess.check_output("/home/jkyle/GBT-ADQ/mysql/blc/blc01")
#print(BLC01[0:5])
#print(BLC01[5:].strip("\n"))
print(BLC01[0:5].strip("\n") + ",host=" + BLC01[5:].strip("\n") +
        ",region=us value=1")
BLC02 = subprocess.check_output("/home/jkyle/GBT-ADQ/mysql/blc/blc02")
#print(BLC02[0:5])
#print(BLC02[5:].strip("\n"))
print(BLC02[0:5].strip("\n") + ",host=" + BLC02[5:].strip("\n") +
        ",region=us value=1")
BLC03 = subprocess.check_output("/home/jkyle/GBT-ADQ/mysql/blc/blc03")
#print(BLC03[0:5])
#print(BLC03[5:].strip("\n"))
print(BLC03[0:5].strip("\n") + ",host=" + BLC03[5:].strip("\n") +
        ",region=us value=1")
BLC04 = subprocess.check_output("/home/jkyle/GBT-ADQ/mysql/blc/blc04")
#print(BLC04[0:5])
#print(BLC04[5:].strip("\n"))
print(BLC04[0:5].strip("\n") + ",host=" + BLC04[5:].strip("\n") +
        ",region=us value=1")
BLC05 = subprocess.check_output("/home/jkyle/GBT-ADQ/mysql/blc/blc05")
#print(BLC05[0:5])
#print(BLC05[5:].strip("\n"))
print(BLC05[0:5].strip("\n") + ",host=" + BLC05[5:].strip("\n") +
        ",region=us value=1")
BLC06 = subprocess.check_output("/home/jkyle/GBT-ADQ/mysql/blc/blc06")
#print(BLC06[0:5])
#print(BLC06[5:].strip("\n"))
print(BLC06[0:5].strip("\n") + ",host=" + BLC06[5:].strip("\n") +
        ",region=us value=1")
BLC07 = subprocess.check_output("/home/jkyle/GBT-ADQ/mysql/blc/blc07")
#print(BLC07[0:5])
#print(BLC07[5:].strip("\n"))
print(BLC07[0:5].strip("\n") + ",host=" + BLC07[5:].strip("\n") +
        ",region=us value=1")
