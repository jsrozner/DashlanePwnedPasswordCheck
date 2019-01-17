# DashlanePwnedPasswordCheck
Check dashlane password data against pwned password API

For use with https://www.troyhunt.com/ive-just-launched-pwned-passwords-version-2/
API at: https://haveibeenpwned.com/API/v2#PwnedPasswords

Dashlane password manager does not offer integration with Troy's pwnedpassword API. This bit of code 
allows users to check their own passwords against the API using python.

Steps to use:
1) Clone the repository
2) Export your dashlane data to a local json file
3) Update example_config.yml to point to your own dashlane json file
4) Run main.py 

Output:
Program will print to stdout any compromised accounts

Test:
Test of the API checker is offered using an example password which will fail.


This program should not leak any personal data anywhere. It keeps all passwords local and submits only the first 5 characters of
the SHA1 hash to the pwnedpassword API. You can read more about the API and k-anonymity online.


I have run the program myself over my own data but make no other guarantees as to the program's validity or safety!

For other users, this code could be used for any sort of spreadsheet or text file. Just change how main.py reads the input data.
