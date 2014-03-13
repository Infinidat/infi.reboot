Overview
========

A cross-platform module for handling reboot-pending operations.
For example, if you did an operation on the OS that:
+ You must not run that operation twice, unless you rebooted the system in between
+ There is no way to determine if the operation has been done since the last reboot

If so, this module is for you.

Usage
-----

Here's an example on how to use this module:

```python
from infi.reboot import ask_for_reboot, has_reboot_took_place
def dangerous_operation():
    raise NotImplementedError()
key = 'my_reboot_request'
if has_reboot_took_place(key):
    dangerous_operation()
    ask_for_reboot(key)
```

Checking out the code
=====================

Run the following:

    easy_install -U infi.projector
    projector devenv build
