fingerprint
-----------
By Matthew Eads

SUMMARY
-------

This is a music processing program written in Python. It takes most formats
of music as input, and will write a .txt file containing the fingerprint of
the music file in ascii text. 

USAGE
-----

To fingerprint a song:
<code>python fingerprint.py parklife.mp3</code>
This will write the fingerprint 'parklife.txt' to the current directory.

To choose a different location/name for the output:
<code>python fingerprint.py -o mode-audio/not-parklife.txt parklife.mp3</code>

To fingerprint all the music files in a directory:
<code>python fingerprint.py -d ~/music/Beatles/</code>

To only fingerprint the first 5 files in a directory:
<code>python fingerprint.py -d ~/music/Beatles/ -c 5</code>

To only fingerprint files 3-6 in a directory:
<code>python fingerprint.py -d ~/music/Beatles/ -c 3-6</code>
The -c option can only be used when -d is also used.

To fingerprint files 2-4 in a directory, and output to a different directory:
<code>python fingerprint.py -d ~/music/Beatles -c 2-4 -o ../not-beatles/</code>

ALGORITHM IN DETAIL
-------------------

fingerprint.py takes the fingerprinting algorithm from [dejavu](https://github.com/worldveil/dejavu), and its [corresponding article](http://willdrevo.com/fingerprinting-and-audio-recognition-with-python/).
In short, a file is extracted into PCM format and sent through a series of 
Fourier Transforms, to get frequency and amplitude over time. This is then
analyzed to find local maxima - peaks in amplitude corresponding to the
'interesting' bits of the track. The resulting data is simply a list of
frequencies over time. This data is the fingerprint - the characteristic
set of frequencies of the song. The frequencies are then written to a file
as ascii text, for use by classify.py. 

VERSION HISTORY AND RELEASE NOTES
---------------------------------
8/2/15 VERSION 0.1.0
  - Initial release
