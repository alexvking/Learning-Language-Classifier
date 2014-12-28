SIMPLE LANGUAGE CLASSIFIER
--------------------------
By Alex King


SUMMARY
-------

This is a text classifier written in Python, previously written in
Racket and later C. It relies on a stored body of "language training" 
documents to build its reference system. See "MODIFYING AND EXTENDING THE 
REFERENCE SYSTEM" below for information on how to add additional classification
modes.

classify provides three example classification modes: language, subject and code.

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

<code>--code</code> will envoke code mode, which recognizes source code files
of the following types:
  - C/C++
  - C#
  - COBOL
  - Java
  - Lisp Family
  - Objective-C
  - Python

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
  - <code>--lang http://lemonde.fr</code> will classify a popular French newspaper
  as French.
  - <code>--subject http://bigocheatsheet.com</code> will classify the site as Computer Science!
  - <code>--subject http://nytimes.com</code> will classify the New York Times as Economics.

NEW IN VERSION 0.7.0: Upon classification, classify will ask the user if the 
classification is correct or not. In the event that it isn't, classify will ask
permission to copy the input file (or html document) into the training library
to strengthen its classification. This is a powerful feature that allows for rapid
improvement. As soon as a hole is found in the training models, the hole can be
partially plugged with the provided document. In theory, after many runs of this
program, the training library could become incredibly strong.

ALGORITHM IN DETAIL
-------------------

classify is an example of simple machine learning that leads to an oddly powerful
end result. The goal is to classify ASCII text into some sort of type within a
category. The provided categories are natural language, programming language, and
academic subject. To do this, classify must have a method of creating a model for
each type within a category, and a model for the input document. Then, classify
must have a method of comparing the predefined models to input to guess what
type is correct.

To generate models, classify uses databases of "trigrams" instead of a 
database of words. This idea came from an assignment from Norman Ramsey's COMP 50 
course at Tufts University in Fall 2013. Please note that the natural language
training documents are also from that course. 

A trigram is a string of three contiguous characters from input.
For example, "Hello!" would yield the trigrams "Hel", "ell", "llo", and "lo!".
Trigrams allow for granular recognition of roots, prefixes, suffixes, and
generally discipline-specific terminology.

Trigrams are counted and summed as an association list, in this case a Python
dictionary. Though counting the number of occurrences of a trigram isn't strictly
necessary for model comparison, (versus just checking if the trigram occurs at all), 
it is a useful step for other data crunching purposes.

After models are generated, the input model is compared to each type's model
within the specified category. For example, if a user runs classify --subject
on a provided Economics document, classify will check the document against its
models for Psychology, Biology, Computer Science and Economics. Model similarity
is derived from bit vector similarity -- essentially summing the number of similar
trigrams between two models, and dividing by the size of the model. A perfect score of 1.0
indicates two identical models, while a score of 0 indicates two completely unrelated models
with no common trigrams. Depending on the training library and input, most comparisons
yield scores between 0.2 and 0.6.

MODIFYING AND EXTENDING THE REFERENCE SYSTEM
--------------------------------------------

classify's quality is limited only by its training corpus. A larger variety of
documents will lead to more accurate classifications. A mode can be added or
changed very easily by adding directories and files in the following format:

  - A directory with name of "mode-<your-mode>" in same directory as classify.py 
  - Within mode directory, directories named after different types within mode
  - Within each type, plain text files representing the type

See folders "mode-lang" and "mode-subject" for examples.

classify will <b>automatically recognize the new mode</b> and it will be usable
from the command line with the expected <code>--mode</code> switch.

Also note that the reference system can be bolstered one document at a time by
"training" it upon incorrect classification (see USAGE above).

KNOWN ISSUES AND PLANNED IMPROVEMENTS
-------------------------------------

As of Version 0.7.0, classify has evolved into more of a proof of concept of 
simple machine learning than a tool focused on practical utility. Language
recognition is generally very accurate due to the great training library provided,
but subject and code recognition exist mostly as proofs of concept now. There
are no immediate plans to bolster their training libraries, because it can now
be done easily through the program itself.

The next step is to add handling of new types within a mode. For instance, if one
were to attempt and classify an Astronomy document, the user could tell classify
that it was not one of the preexisting types, but rather a new one entirely. This
would make it very fast to categorize a lot of different documents, particularly
websites.

Other issues (pre-0.7.0:)

classify currently has no way of knowing if the supplied text is in English for
the <code>--subject</code> option, so it may silently give wrong answers.

A simple GUI with rich file selection would be a great next step for this
software. It could also be extended easily to work on programming languages.

More academic subjects may be added soon. There is no obvious way to find a 
random sampling of various material, so this work is tedious. It exists as an
option right now as a proof of concept more than anything else. Same goes for 
the code mode.


VERSION HISTORY AND RELEASE NOTES
---------------------------------

12/28/14 VERSION 0.7.0
  - Added ability to "train" the classifier upon incorrect classification by
    copying input file (or website) to the training library. This is a big next
    step that turns classify into more of an example of machine learning.

12/22/14 VERSION 0.6.5

  - Added automatic recognition of modes to make it easy to extend classify's
    usability. Usage switches will be automatically recognized.
  - Added <code>--code</code> as another experimental option. The reference 
    material, taken from rosettacode.org, is currently very limited.

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
