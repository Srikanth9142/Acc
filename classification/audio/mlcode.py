from python_speech_features import mfcc,delta,logfbank 
import numpy
import scipy.io.wavfile
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import wave
import contextlib
from scipy.fftpack import dct
import scipy.io.wavfile as wav
from tensorflow import keras
from keras.models import load_model
import tensorflow as tf

# Fixed variables used in mfcc
pre_emphasis = 0.97
frame_size = 0.025
frame_stride = 0.01
NFFT = 512
nfilt = 40
num_ceps = 12
cep_lifter =22


#Returns a duration of audio file which needs to send every 3 seconds audio to mfcc
def length_audio(file_name):
    file_path='./media/audio/'+str(file_name)
    with contextlib.closing(wave.open(file_path,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
    return int(duration)

def create_mfcc(file_name,start_point):
    file_path = './media/audio/'+str(file_name)
    sample_rate, signal = scipy.io.wavfile.read(file_path)
    signal = signal[start_point:int(start_point+3 * sample_rate)]   #framing to 3 seconds
    emphasized_signal = numpy.append(signal[0], signal[1:] - pre_emphasis * signal[:-1])
    frame_length, frame_step = frame_size * sample_rate, frame_stride * sample_rate  # Convert from seconds to samples
    signal_length = len(emphasized_signal)
    frame_length = int(round(frame_length))
    frame_step = int(round(frame_step))
    num_frames = int(numpy.ceil(float(numpy.abs(signal_length - frame_length)) / frame_step))  # Make sure that we have at least 1 frame
    pad_signal_length = num_frames * frame_step + frame_length
    z = numpy.zeros((pad_signal_length - signal_length))
    pad_signal = numpy.append(emphasized_signal, z) # Pad Signal to make sure that all frames have equal number of samples without truncating any samples from the original signal
    indices = numpy.tile(numpy.arange(0, frame_length), (num_frames, 1)) + numpy.tile(numpy.arange(0, num_frames * frame_step, frame_step), (frame_length, 1)).T
    frames = pad_signal[indices.astype(numpy.int32, copy=False)]
    frames *= numpy.hamming(frame_length)  #hamming window
    mag_frames = numpy.absolute(numpy.fft.rfft(frames, NFFT))  # Magnitude of the FFT
    pow_frames = ((1.0 / NFFT) * ((mag_frames) ** 2))  # Power Spectrum
    low_freq_mel = 0
    high_freq_mel = (2595 * numpy.log10(1 + (sample_rate / 2) / 700))  # Convert Hz to Mel
    mel_points = numpy.linspace(low_freq_mel, high_freq_mel, nfilt + 2)  # Equally spaced in Mel scale
    hz_points = (700 * (10**(mel_points / 2595) - 1))  # Convert Mel to Hz
    bin = numpy.floor((NFFT + 1) * hz_points / sample_rate)
    fbank = numpy.zeros((nfilt, int(numpy.floor(NFFT / 2 + 1))))
    for m in range(1, nfilt + 1):
        f_m_minus = int(bin[m - 1])   # left
        f_m = int(bin[m])             # center
        f_m_plus = int(bin[m + 1])    # right
        for k in range(f_m_minus, f_m):
            fbank[m - 1, k] = (k - bin[m - 1]) / (bin[m] - bin[m - 1])
        for k in range(f_m, f_m_plus):
            fbank[m - 1, k] = (bin[m + 1] - k) / (bin[m + 1] - bin[m])
    filter_banks = numpy.dot(pow_frames, fbank.T)
    filter_banks = numpy.where(filter_banks == 0, numpy.finfo(float).eps, filter_banks)  # Numerical Stability
    filter_banks = 20 * numpy.log10(filter_banks)  # dB
    mfcc = dct(filter_banks, type=2, axis=1, norm='ortho')[:, 1 : (num_ceps + 1)] # Keep 2-13
    (nframes, ncoeff) = mfcc.shape
    n = numpy.arange(ncoeff)
    lift = 1 + (cep_lifter / 2) * numpy.sin(numpy.pi * n / cep_lifter)
    mfcc *= lift  #*
    
    filter_banks -= (numpy.mean(filter_banks, axis=0) + 1e-8)
    mfcc -= (numpy.mean(mfcc, axis=0) + 1e-8)
    
    return mfcc


def create_model():
    model = keras.Sequential([
    keras.layers.Flatten(input_shape=(7176,)),
    keras.layers.Dense(40,activation=tf.nn.relu),
    keras.layers.Dense(10,activation=tf.nn.relu),
    keras.layers.Dense(13, activation=tf.nn.softmax)
    ])

    model.compile(optimizer='adam',loss='sparse_categorical_crossentropy',metrics=['accuracy'])
    return model


def predictAccent(targ):
    accents = ['Indian','US-Male','US-Female','British','Mild Generic Indian','Mild Hindi','Mild Tamil','Neutral Indian','Strong Bengali','Strong Hindi','Strong Tamil','Strong Telugu']
    l=[]
    str_acc=""
    out_len = len(targ)
    in_len = len(targ[0])
    for i in range(in_len):
        sumi = 0
        for j in range(out_len):
            sumi+=targ[j][i]
        l.append(sumi)
    maximum = -1
    max_ind = -1
    for i in range(len(l)):
        if(l[i] > maximum):
            maximum = l[i]
            max_ind = i+1
    print("Accent: ",accents[max_ind-2])
    str_acc+="Your Accent: "
    str_acc+=accents[max_ind-2]
    str_acc+="\n"
    for i in l:
        if i!=0:
            per = (i/float(out_len))*100
            if(per>1):
                per = "{:.2f}".format(per)+"%"
                str_acc+=accents[l.index(i)-1]+" --> "
                str_acc+=per
                str_acc+="\n"
    return str_acc

def predictAudio(filename):
    n = filename
    mfcc=[] 
    target=[]
    mfcc_len=length_audio(n)
    for i in range(0,mfcc_len,3):
        mfcc = create_mfcc(n,i)
        mfcc = np.asarray(mfcc)
        mfcc = np.reshape(mfcc,(len(mfcc)*len(mfcc[0])))
        target.append(mfcc)
    target=np.asarray(target)
    md = create_model()
    md.load_weights('./Mlmodel/accent classification.h5')
    targ=md.predict(target)
    acc_str = predictAccent(targ)
    return acc_str


def getPassage(index):
    passages = ['I walked along the winding trail,the dog running before me,my wife next to me,with cliffs to one side,and a river to the other.Tall grasses, as tall as me,and evergreen trees, everywhere.The wind blew gentle,as grey clouds drifted by,and I pondered existence.',
              'Temperatures rose, sea level too.Melting glaciers flooded more land.Some struggled to reduce emissions.Others shrugged, undaunted by growing evidenceOf fires, floods, and environmental chaos.',
              'The cat walks away, padding across the floor, its rough tongue sanding the red around its chops. Behind it, the pigeon lies in a carpet of feathers, waiting for the cleaning lady to sweep her lifeless body into the big blue dustbin. In a nest, two eggs wait for warmth.',
              'She had attempted to ignore him, hoping he wouldn’t approach her as she stood alone in the aisle of the bookstore. He was the persistent kind, though.After approaching her, he mustered a polite smile and blinked twice.“Excuse me,” she said by way of introduction, gently fanning behind herself.',
              'A mummy works Macy’s gift wrap counter. He told the boss he has 2,000 years in wrapping. Sometimes his hands get confused and he realizes he’s using bandages from his arm. Unspools. Starts over. Customers curse, but he isn’t bothered by curses, and he has all the time in the world.',
              '“When will I see mommy?” Clare would ask everyday.“Before you head to bed, honey” Auntie would reply.Those words echoed in her ear as her eyes pleaded to be closed.This time,her mother made it. Just before the monitor flat-lined.Melancholy spread as Clare finally slept with a smile.'
              ]
    return passages[index]