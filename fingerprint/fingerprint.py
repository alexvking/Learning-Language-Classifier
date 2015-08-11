import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import (generate_binary_structure,
                                      iterate_structure, binary_erosion)
from operator import itemgetter
import os
import fnmatch
import numpy as np
import pydub
from pydub import AudioSegment
from pydub.utils import audioop
import wave
from hashlib import sha1
import sys
import glob

# Minimum amplitude in spectrogram in order to be considered a peak.
# This can be raised to reduce number of fingerprints, but can negatively
# affect accuracy.
DEFAULT_AMP_MIN = 10

# Number of cells around an amplitude peak in the spectrogram in order
# for Dejavu to consider it a spectral peak. Higher values mean less
# fingerprints and faster matching, but can potentially affect accuracy.
PEAK_NEIGHBORHOOD_SIZE = 20

def read(filename, limit=None):
    #    """
    #    Reads any file supported by pydub (ffmpeg) and returns the data contained
    #    within. If file reading fails due to input being a 24-bit wav file,
    #    wavio is used as a backup.
    #
    #   Can be optionally limited to a certain amount of seconds from the start
    #    of the file by specifying the `limit` parameter. This is the amount of
    #    seconds from the start of the file.
    
    #    returns: (channels, samplerate)
    #    """
    # pydub does not support 24-bit wav files, use wavio when this occurs
    try:
        audiofile = AudioSegment.from_file(filename)

        if limit:
            audiofile = audiofile[:limit * 1000]

        data = np.fromstring(audiofile._data, np.int16)

        channels = []
        for chn in xrange(audiofile.channels):
            channels.append(data[chn::audiofile.channels])

        fs = audiofile.frame_rate
    except audioop.error:
        fs, _, audiofile = wavio.readwav(filename)

        if limit:
            audiofile = audiofile[:limit * 1000]

        audiofile = audiofile.T
        audiofile = audiofile.astype(np.int16)

        channels = []
        for chn in audiofile:
            channels.append(chn)
    except pydub.exceptions.CouldntDecodeError:
        return ([], 0)

    return channels, audiofile.frame_rate



def fingerprint(channel_samples):
    """
    FFT the channel, log transform output, find local maxima, then return
    locally sensitive hashes.
    """
    # FFT the signal and extract frequency components
    arr2D = mlab.specgram(
        channel_samples)[0]

    # apply log transform since specgram() returns linear array
    arr2D = 10 * np.log10(arr2D)
    arr2D[arr2D == -np.inf] = 0  # replace infs with zeros

    # find local maxima
    local_maxima = get_2D_peaks(arr2D, plot=False)
    return local_maxima

def get_2D_peaks(arr2D, plot=False, amp_min=DEFAULT_AMP_MIN):
    # http://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.morphology.iterate_structure.html#scipy.ndimage.morphology.iterate_structure
    struct = generate_binary_structure(2, 1)
    neighborhood = iterate_structure(struct, PEAK_NEIGHBORHOOD_SIZE)

    # find local maxima using our fliter shape
    local_max = maximum_filter(arr2D, footprint=neighborhood) == arr2D
    background = (arr2D == 0)
    eroded_background = binary_erosion(background, structure=neighborhood,
                                       border_value=1)

    # Boolean mask of arr2D with True at peaks
    detected_peaks = local_max - eroded_background

    # extract peaks
    amps = arr2D[detected_peaks]
    j, i = np.where(detected_peaks)

    # filter peaks
    amps = amps.flatten()
    peaks = zip(i, j, amps)
    peaks_filtered = [x for x in peaks if x[2] > amp_min]  # freq, time, amp

    # get indices for frequency and time
    frequency_idx = [x[1] for x in peaks_filtered]
    time_idx = [x[0] for x in peaks_filtered]

    if plot:
        # scatter of the peaks
        fig, ax = plt.subplots()
        ax.imshow(arr2D)
        ax.scatter(time_idx, frequency_idx)
        ax.set_xlabel('Time')
        ax.set_ylabel('Frequency')
        ax.set_title("Spectrogram")
        plt.gca().invert_yaxis()
        plt.show()
    zippy = zip(frequency_idx, time_idx)
    zippy.sort(key=lambda tup: tup[1])
    return zippy

def usage():
    print "Usage: python fingerprint.py [options] [song]"
    sys.exit(1)

if len(sys.argv) == 2:
    songname = sys.argv[1]
    if not os.path.exists(songname):
        print "Song not found"
        print "Usage: python fingerprint.py [options] [song]"
        sys.exit(1)
    channels, Fs = read(songname)
    #for x in xrange(len(channels[0])):
    #    channel_samples.append(np.mean((channels[0][x],channels[1][x])))
    if channels:
        channel_samples = channels[0]
        zippy = fingerprint(channel_samples)
        text = ""
        for x in zippy:
            text += chr(x[0])
        #print text
        file = open(songname[:(len(songname) - 3)] + 'txt', 'w')
        file.write(text)
        file.close()

elif len(sys.argv) > 2:
    options = sys.argv[1:]
    i = 1
    dir_mode = False
    file_count = False
    output_specified = False
    while i < len(sys.argv) - 1:
        if sys.argv[i] == "-d":
            dir_mode = True
            if sys.argv[i+1][0] == '-':
                usage()
            directory = sys.argv[i+1]
            i += 1
        elif sys.argv[i] == "-c":
            file_count = True
            if sys.argv[i+1][0] == '-':
                usage()
            if sys.argv[i+1].count('-') == 1:
                offset_count = True
                str = sys.argv[i+1].split('-')
                offset = int(str[0])
                count = int(str[1])
            else:
                count = int(sys.argv[i+1])
            i += 1
        elif sys.argv[i] == "-o":
            output_specified = True
            if sys.argv[i+1][0] == '-':
                usage()
            output = sys.argv[i+1]
            i += 1
        else:
            usage()
        i += 1

    if file_count and not dir_mode:
        print "Directory mode must be used when proiding a number of files"
        usage()
    elif dir_mode:
        if not os.path.exists(directory):
            print "Directory not found"
            print "Usage: python fingerprint.py -d [input dir]"
            sys.exit(1)
        if directory[len(directory) - 1] != '/':
            directory += '/'

        songs = glob.glob(directory + '*.*')
        i = 1
        print songs
        for song in songs:
            channels, Fs = read(song)
            if file_count and i > count:
                break
            if offset_count and i < offset:
                continue
            if channels:
                zippy = fingerprint(channels[0])
                text = ""
                for x in zippy:
                    text += chr(x[0])
                if output_specified:
                    if output[len(output) -1] != '/':
                        output += '/'
                    if not os.path.exists(output):
                        os.makedirs(output)
                    song = song.rsplit('/', 1)[1]
                    outfile = output + song[:len(song)-3] + 'txt'
                else:
                    song = song.rsplit('/', 1)[1]
                    outfile = song[:len(song)-3] + 'txt'
#                outfile = outfile.rsplit('/', 1)[1]
                file = open(outfile, 'w')
                file.write(text)
                file.close()
                i += 1
    else:
        songname = sys.argv[len(sys.argv) - 1]
        if not os.path.exists(songname):
            print "Song not found"
            print "Usage: python fingerprint.py [options] [song]"
            sys.exit(1)
        channels, Fs = read(songname)
        #for x in xrange(len(channels[0])):
        #    channel_samples.append(np.mean((channels[0][x],channels[1][x])))
        if channels:
            channel_samples = channels[0]
            zippy = fingerprint(channel_samples)
            text = ""
            for x in zippy:
                text += chr(x[0])
            outfile = songname[:len(songname)-3] + 'txt'
            if output_specified:
                outfile = output
            file = open(outfile, 'w')
            file.write(text)
            file.close()
            
else:
    sys.stdout.write("Usage: python fingerprint.py [options] song\n")
    sys.exit(1)
