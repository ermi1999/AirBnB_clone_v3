# HBNB - The Console
The console is the first segment of the AirBnB project at Holberton School that will collectively cover fundamental concepts of higher level programming. The goal of the console is to manage the objects of the project:

- Create a new object (ex: a new User or a new Place)
- Retrieve an object from a file, a database etc...
- Do operations on objects (count, compute stats, etc...)
- Update attributes of an object
- Destroy an object

## Usage
The console can be run in interactive mode:
$ ./console.py
(hbnb) help

Documented commands (type help <topic>):
EOF all create destroy help quit show update

(hbnb)
(hbnb) quit
$
But also in non-interactive mode:
$ echo "help" | ./console.py
(hbnb)
Documented commands (type help <topic>):
EOF all create destroy help quit show update
(hbnb)
$
$ cat test_help
help
$ ./console.py < test_help
(hbnb)
Documented commands (type help <topic>):
EOF all create destroy help quit show update
(hbnb)
$

scheme

Copy

## Bugs
No known bugs at this time.

## Authors
Alexa Orrico - [Github](https://github.com/alexaorrico) / [Twitter](https://twitter.com/alexa_orrico)
Jennifer Huang - [Github](https://github.com/jhuang10123) / [Twitter](https://twitter.com/earthtojhuang)
Joann Vuong - [Github](https://github.com/joannvu) / [Twitter](https://twitter.com/JoannVuong)

## New Contribution
I, Joann Vuong, have added the functionality to the console to allow users to create, list, show, update, and destroy instances of the `BaseModel` class. This includes the implementation of the `create`, `show`, `destroy`, `all`, and `update` commands, which provide a user-friendly interface for interacting with the AirBnB project's objects.

## License
Public Domain. No copyright protection.

