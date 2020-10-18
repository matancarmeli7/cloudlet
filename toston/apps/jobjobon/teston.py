import sys
import os

the_message = os.getenv('BIG_MSG')

print(the_message)

if "err" not in the_message:
    sys.exit(0)
else:
    sys.exit(1)

