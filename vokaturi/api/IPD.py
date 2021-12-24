# OpenVokaWavMean-win64.py
# public-domain sample code by Vokaturi, 2020-02-20
#
# A sample script that uses the VokaturiPlus library to extract the emotions from
# a wav file on disk. The file has to contain a mono recording.
#
# Call syntax:
#   python3 OpenVokaWavMean-win64.py path_to_sound_file.wav
#
# For the sound file hello.wav that comes with OpenVokaturi, the result should be:
#	Neutral: 0.760
#	Happy: 0.000
#	Sad: 0.238
#	Angry: 0.001
#	Fear: 0.000

import sys
import scipy.io.wavfile

sys.path.append("../api")
import Vokaturi

def analyse_audio(path):
    print("Loading library...")
    Vokaturi.load(r"C:\Users\vighn\Desktop\mhw\vokaturi\lib\open\win\OpenVokaturi-3-4-win64.dll")
    print("Analyzed by: %s" % Vokaturi.versionAndLicense())

    print("Reading sound file...")

    (sample_rate, samples) = scipy.io.wavfile.read(path)
    print("   sample rate %.3f Hz" % sample_rate)

    print("Allocating Vokaturi sample array...")
    buffer_length = len(samples)
    print("   %d samples, %d channels" % (buffer_length, samples.ndim))
    c_buffer = Vokaturi.SampleArrayC(buffer_length)
    if samples.ndim == 1:  # mono
        c_buffer[:] = samples[:] / 32768.0
    else:  # stereo
        c_buffer[:] = 0.5*(samples[:, 0]+0.0+samples[:, 1]) / 32768.0

    print("Creating VokaturiVoice...")
    voice = Vokaturi.Voice(sample_rate, buffer_length)

    print("Filling VokaturiVoice with samples...")
    voice.fill(buffer_length, c_buffer)

    print("Extracting emotions from VokaturiVoice...")
    quality = Vokaturi.Quality()
    emotionProbabilities = Vokaturi.EmotionProbabilities()
    voice.extract(quality, emotionProbabilities)

    if quality.valid:
        print("Neutral: %.3f" % (emotionProbabilities.neutrality*100))
        print("Happy: %.3f" % (emotionProbabilities.happiness*100))
        print("Sad: %.3f" % (emotionProbabilities.sadness*100))
        print("Angry: %.3f" % (emotionProbabilities.anger*100))
        print("Fear: %.3f" % (emotionProbabilities.fear*100))
    else:
        print("Not enough sonorancy to determine emotions")

    voice.destroy()
