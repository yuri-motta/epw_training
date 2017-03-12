import os

os.system('ffplay -fflags nobuffer -flags low_delay -framedrop -strict experimental udp://200.129.152.73:4445')