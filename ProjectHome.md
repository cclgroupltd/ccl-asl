ccl\_asl is a small Python module for dealing with ASL (Apple System Log)/ASLDB files.

The module comprises a class library for accessing the records in your code (the AslDb class implements`'__iter__`, `__len__`, `__getitem__`) and also a command-line interface for dumping the contents of logs to TSV files (other formats would be trivial to add).

The repository also contains a couple of examples of the module in use to parse battery usage from an iOS device, and a login, boot, shutdown, etc. timeline from OSX.

A blog explaining the file structure can be found here: http://digitalinvestigation.wordpress.com/2012/06/18/parsing-apple-system-log-files-osx-ios/

_To download the scripts go to the "Source" tab and click "Browse"_


---


### Other projects ###
  * http://code.google.com/p/ccl-bplist/ - ccl\_bplist: Python module for parsing Binary Property List files
  * http://code.google.com/p/ccl-ipd/ - ccl\_ipd: Python module for parsing BlackBerry IPD backup files
  * http://code.google.com/p/ccl-ssns/ - ccl\_ssns: Python module and command line interface for parsing Chrome session files (Last Tabs, Current Session, etc.)