
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


# In[7]:

import subprocess
newline = None

Test1 = subprocess.run(["echo", "'select ant_motion from status;'",
                        "|", "mysql", "-h", "gbtdata.gbt.nrao.edu", "-u",
                        "gbtstatus", "--password=w3bquery", "-E",
                        "gbt_status"], 
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
print("{Test1.stdout}".format(Test1=Test1))


# In[42]:

import subprocess
from subprocess import Popen, PIPE

Test1 = subprocess.Popen(["echo", "'hello'"], 
                       stdout=PIPE)

out, err = Test1.communicate()
print(out)





# In[ ]:



