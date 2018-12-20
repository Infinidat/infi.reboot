Overview
========

A cross-platform module for handling reboot-pending operations.
For example, if you need to run an operation on the OS that:
+ Must not be run twice, unless the system was rebooted in between
+ There is no way to determine if the operation has been run since the last reboot

Then this module is for you.

Usage
-----

Here's an example on how to use this module:

```python
from infi.reboot import ask_for_reboot, has_reboot_taken_place
def dangerous_operation():
    raise NotImplementedError()
key = 'my_reboot_request'
if has_reboot_taken_place(key):
    dangerous_operation()
    ask_for_reboot(key)
```

Checking out the code
=====================

Run the following:

    easy_install -U infi.projector
    projector devenv build

Python 3
========

Support for Python 3 is experimental at this stage
