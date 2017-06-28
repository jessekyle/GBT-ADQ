
# coding: utf-8

# In[ ]:

import subprocess

Test8 = subprocess.list2cmdline(["echo", "'select ant_motion from status;'",
                                "|", "mysql", "-h", "gbtdata.gbt.nrao.edu", "-u",
                                "gbtstatus", "--password=w3bquery", "-E",
                                "gbt_status"])

answer = subprocess.getoutput(Test8)

if answer == "ant_motion: Slewing":
    print("Slewing")
elif answer == "ant_motion: Guiding":
    print("Guiding")
else:
    print("Not Slewing or Guiding")

