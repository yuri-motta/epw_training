import os

"""no client deve-se colocar o seu proprio ip"""

os.system('ffplay -fflags nobuffer -flags low_delay -framedrop -strict experimental udp://127.0.0.1:4445')