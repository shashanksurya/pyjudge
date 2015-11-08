pyjudge
=======

Instant judgement of python scripts.

Limitation
-------------

For now, it is only accessible from the localhost.

Running the server:
-------------------

python server.py

Adding tests:
-------------

Create a directory named with the problem number. Add test cases and expected output as text files into the directory.

Test cases: input_0.dat
output:     output_0.txt

E.g.:

..
  1/
    --> input_0.dat
    --> output_0.txt
    --> input_1.dat
    --> output_1.txt

Submitting program:
-------------------

./submit_program <prob_no> <file_name>


Testing on the sample problem 1:
================================

Just do the following:

./submit_program 1 prob_1.py

But make sure the server is up.

The server now supports the web module, starting the server will be the same.
For admin or user module, login on the page:
http://localhost:5000/login

You can login as admin using : jobi1 and pass: 123 
You can login as user using: st13f and pass:123

---Password hashing disabled temporarily, needs to be enabled before deploying---