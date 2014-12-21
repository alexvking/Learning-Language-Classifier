SIMPLE LANGUAGE CLASSIFIER
--------------------------
By Alex King


SUMMARY
-------

This is a basic language classifier written in Python, previously created in
Racket and later C. It relies on a predefined body of "language training" 
documents to build its reference system. See "MODIFYING AND EXTENDING THE 
REFERENCE SYSTEM" below for information on how to add additional training
material.

The classifier works in two main modes: language and subject.

<code>--lang</code> will envoke language mode, which recognizes input text in the following
languages:
  - Czech
  - English
  - French
  - German
  - Hungarian
  - Italian
  - Polish
  - Russian
  - Spanish

<code>--subject</code> will envoke subject mode, which expects an academic paper (or similar)
written in English, and will recognize the following subjects of study:
  - Computer Science
  - Biology
  - Psychology
  - Economics

The comparison is speedy and surprisingly accurate at this point in time. Even
better, it is only about 100 lines of code.


USAGE
-----

classify expects either plain formatted text specified as a file or a web address
from the command line.

To run language recognition, run with <code>python classify.py --lang [input.txt|http://webpage.com]</code>.

To run academic subject recognition, run with <code>--subject</code> instead.

It is convenient to run <code>pdftotext [paper.pdf]</code> to extract plain text from an
academic paper formatted as pdf.

Examples:

  - <code>--lang samples/polish.txt</code> will classify a Polish text as Polish.
  - <code>--subject samples/econ6.txt</code> will classify an Economics paper as Economics.
  - <code>--lang http://google.com</code> will classify the Google homepage as English.
  - <code>--subject http://bigocheatsheet.com</code> will classify the site as Computer Science!
  - <code>--subject http://nytimes.com</code> will classify the New York Times as Economics.


ALGORITHM
---------

classify uses databases of "trigrams" instead of a database of words. This idea
came from an assignment from Norman Ramsey's COMP 50 class at Tufts University
in Fall 2013. A trigram is a string of three contiguous characters from input.
For example, "Hello!" would yield the trigrams "Hel", "ell", "llo", and "lo!".

Trigrams allow for granular recognition of roots, prefixes, suffixes, and
generally discipline-specific terminology. Because of this, classify is able
to notice patterns and trends and, in addition to being a reliable language
recognizer, can make a good guess at the academic subject of English input.


MODIFYING AND EXTENDING THE REFERENCE SYSTEM
--------------------------------------------

classify's quality is limited only by its training corpus. A larger variety of
documents will lead to more accurate classifications. A mode can be added or
changed by adding directories and files in the following format:

  - A directory with name of mode in same directory as classify.py 
  - Within mode directory, directories named after different types within mode
  - Within each type, plain text files representing the type

See folders "lang" and "subject" for examples. Execution options must be added
through the <code>main()</code> function, but all other looping and naming should happen
automatically.


KNOWN ISSUES AND PLANNED IMPROVEMENTS
-------------------------------------

classify currently has no way of knowing if the supplied text is in English for
the <code>--subject</code> option, so it may silently give wrong answers.

A simple GUI with rich file selection would be a great next step for this
software. It could also be extended easily to work on programming languages.

More academic subjects should be added soon. There is no obvious way to find a 
random sampling of various material, so this work is tedious.


VERSION HISTORY AND RELEASE NOTES
---------------------------------

12/20/14 VERSION 0.6.0

  - Added language recognition of web pages. Use a web address beginning with 
    http://.

12/20/14 VERSION 0.5.0

  - Rewritten in Python: a teaching experiment for the author, and an exercise
    in recognizing what Python is so good at. Python has so many convenient
    looping and mapping methods built in, it is far easier to manage directories
    of training documents. The original Racket version was several hundred lines
    of code, the C version was around 250, and the Python version is around 100.
  - Returning support of natural language recognition! Run as option <code>--lang</code>. 
    This was made far easier to implement after porting to Python.

11/15/14 VERSION 0.2.0

  - Support for Economics
  - Initial git commit

11/14/14 VERSION 0.1.0
  - Initial release
  - Support for three subjects: Computer Science, Psychology, Biology
