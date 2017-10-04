import pyaudio
import struct
from pylab import *

class AudioPlayer:
    def __init__(self):
        self.p      = pyaudio.PyAudio()

    def initialize(self,sampleFrequency=44100,numChannels=1):
        self.fs     = sampleFrequency   # integer [Hz]
        self.stream = self.p.open(
                        format  =pyaudio.paFloat32,
                        channels=numChannels,
                        rate    =sampleFrequency,
                        output  =True)
        return self


    def initializeRecord(self,sampleFrequency=44100,numChannels=1,FRAMESIZE=2**2):
        self.FRAMESIZE          = FRAMESIZE
        self.sampleFrequency    = sampleFrequency
        self.recordStream = self.p.open(format=pyaudio.paFloat32,channels=numChannels,rate=sampleFrequency,input=True,frames_per_buffer=FRAMESIZE)

    def record(self,duration,CHUNK = 1024):
        numChunks = int(self.sampleFrequency/CHUNK * duration)
        data = self.recordStream.read(CHUNK*numChunks)
        decodedData = array(struct.unpack(str(CHUNK*numChunks)+'f',data))
        return decodedData

    def constructTimeArray(self,duration):
        return arange(self.fs*duration)/self.fs

    def play(self,signal):
        # note: amplitude [0,1] !!!
        self.stream.write(signal.astype(float32).tostring())

    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()


class Instrument:
    def __init__(self,speaker,beatDuration=1.0,duration=20.):
        self.speaker      = speaker
        self.beatDuration = beatDuration
        self.time         = speaker.constructTimeArray(duration)#beatDuration)
        self.signal       = 0*self.time
        self.toneNarrowing= 0.62
        self.toneUp       = 2**(1./12)
        self.toneDown     = 1./self.toneUp
        self.lastSignal   = 0.0
        # self.harmonicList = [(2,0.25),(3,0.1),(4,0.05)]
        self.harmonicList = [(0.5,0.1),(2,0.25),(3,0.25),(4,0.1)]
        self.fullnotes = ["C","D","E","F","G","A","B"]
        self.notes = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
        self.noteintevals = {
            "C" :(2,-1), #
            "C#":(2,-2),
            "D" :(2,-2),
            "D#":(2,-2),
            "E" :(1,-2), #
            "F" :(2,-1), #
            "F#":(2,-2),
            "G" :(2,-2),
            "G#":(2,-2),
            "A" :(2,-2),
            "A#":(2,-2),
            "B" :(1,-2)} #
        self.freqnames = {
            "."     : 0.0,
            "C"     : 261.63,
            "C#"    : 277.18,
            "D"     : 293.66,
            "D#"    : 311.13,
            "E"     : 329.63,
            "F"     : 349.23,
            "F#"    : 369.99,
            "G"     : 392.00,
            "G#"    : 415.30,
            "A"     : 440.00,
            "A#"    : 466.16,
            "B"     : 493.88,
            "H"     : 493.88}

    def notesUp(self,note,octave,n):
        noteIndex = self.fullnotes.index(note)
        if n>0:
            index = 0
        else:
            index = 1
        f = self.getFreq(note,octave)
        factor = 1
        for i in xrange(abs(int(n))):
            factor *= self.toneUp**(self.noteintevals[note][index])
            if index==0:
                noteIndex += 1
            if index==1:
                noteIndex -= 1
            noteIndex = (noteIndex+len(self.fullnotes))%len(self.fullnotes)
            note = self.fullnotes[noteIndex]
        return factor

    def getFreq(self,name,num=1):
        return self.freqnames[name]*2**(num-4)

    def setHarmonics(self,harmonicList):
        self.harmonicList = harmonicList
        return self

    def setTone(self,freq=440,shift=0.0,window=(0,1e20)):
        t = self.time
        t = t[(t>window[0]-window[1])*(t<window[0]+2*window[1])]
        self.tone = sin(2*pi*freq*t+shift)
        for pair in self.harmonicList:
            multiplum = pair[0]
            amplitude = pair[1]
            freqH = multiplum*freq
            self.tone += amplitude*sin(2*pi*freqH*self.time+shift)
        return self.tone

    def setToneWithCut(self,freq=440,shift=0.0,window=(0,1e20)):
        t = self.time
        cut = (t>window[0]-window[1])*(t<window[0]+2*window[1])
        t = self.time[cut]
        self.tone = sin(2*pi*freq*t+shift)
        for pair in self.harmonicList:
            multiplum = pair[0]
            amplitude = pair[1]
            freqH = multiplum*freq
            self.tone += amplitude*sin(2*pi*freqH*t+shift)
        return cut

    def clearSignal(self):
        self.signal = 0*self.time
        return self

    def gaussianModulator(self,t0,dt):
        modulator = exp(-((self.time-t0)/dt)**4)
        self.tone = self.tone * modulator
        return self.tone

    def sigmoidalModulator(self,t0,dt,s1,s2):
        t = self.time
        # cut = (t>t0-0.3*dt)*(t<t0+dt+0.3*dt)
        modulatorLeft  = 1/(1+exp(-s1*(t-t0)))
        modulatorRight = 1/(1+exp(s2*(t-dt-t0)))
        # modulator = modulator*cut
        self.tone    = self.tone * modulatorLeft*modulatorRight
        return self.tone

    def sigmoidalModulatorOnCut(self,t0,dt,s1,s2,cut):
        t = self.time[cut]
        modulatorLeft  = 1/(1+exp(-s1*(t-t0)))
        modulatorRight = 1/(1+exp(s2*(t-dt-t0)))
        self.tone    = self.tone * modulatorLeft*modulatorRight
        return self.tone

    def addTone(self,f,ti,dt,volume=0.5):
        cut = self.setToneWithCut(freq=f,shift=2*pi*random(),window=(ti,dt))
        toneSignal = volume*self.sigmoidalModulatorOnCut( ti, self.toneNarrowing*dt, 100., 200., cut)
        self.signal[cut] += toneSignal

    def addStrophe(self,num,notes,volume=0.5):
        # notes = [ ... (notename,duration)...]
        # duration can i.e be 8 meaning 1/8th of beatDuration
        ti = (num+1)*self.beatDuration
        for pair in notes:
            if ":" in pair[0]:
                FREQpair = pair[0].split(":")
                FREQ = FREQpair[0]
                FREQoctave = float(FREQpair[-1])
            else:
                FREQ = pair[0]
                FREQoctave = 4. # default C4 ... A4
            f  = self.getFreq(FREQ,FREQoctave)
            dt = self.beatDuration/pair[-1]

            self.addTone(f,ti,dt,volume)

            ti += dt
            if self.lastSignal<ti: self.lastSignal = ti
        return self.signal

    def populateHashList(self,hashList):
        newHash = []
        for entry in hashList:
            newHash.append(entry-2*7)
            newHash.append(entry-7)
            newHash.append(entry)
            newHash.append(entry+7)
            newHash.append(entry+2*7)
        return newHash

    def constructSongFromChords(self,TONES,DURATION,volume=0.5):
        TONES       = TONES.replace(" ","").strip("|").split("|")
        DURATION    = DURATION.replace(" ","").strip("|").split("|")
        for i in xrange(len(TONES)):
            stropheDATA = []
            notes       = TONES[i].split("-")
            durations   = DURATION[i].split("-")
            for j in xrange(len(notes)):
                note        = notes[j]
                duration    = durations[j]
                pair = [note, float(duration)]
                stropheDATA.append( pair )
            print " ".join(notes)
            print " ".join(durations)
            self.addStrophe(i,stropheDATA,volume)

    def constructSongFromNotesheet(self,TONES,DURATION,base=("G",4),volume=0.5,hashkeys=[],atpart=0):
        hashkeys = self.populateHashList(hashkeys)
        basef = self.getFreq(base[0],base[-1])

        TONES       = TONES.replace(" ","").strip("|").split("|")
        DURATION    = DURATION.replace(" ","").strip("|").split("|")
        ti = (1+atpart)*self.beatDuration
        for i in xrange(len(TONES)):
            stropheDATA = []
            notes       = TONES[i].split("_")
            durations   = DURATION[i].split("_")
            for j in xrange(len(notes)):
                if "#" in notes[j]:
                    notes[j] = notes[j].replace("#","")
                    factor = self.toneUp*self.notesUp(base[0],base[1],float(notes[j]))
                else:
                    factor = self.notesUp(base[0],base[1],float(notes[j]))
                if notes[j] in hashkeys:
                    factor *= self.notesUp
                f        = basef*factor#self.toneUp**(2*int(notes[j]))
                duration = float(durations[j])
                dt = self.beatDuration/duration
                self.addTone(f,ti,dt,volume)
                ti += dt
                if self.lastSignal<ti: self.lastSignal = ti


    def trimToLastSignal(self,dt_add):
        cut = self.time<self.lastSignal+dt_add
        self.time   = self.time[cut]
        self.signal = self.signal[cut]

    def play(self):
        self.speaker.play(self.signal)


#
#
# speaker = AudioPlayer()
# speaker.initialize(numChannels=1)
#
# instrument  = Instrument(speaker,duration=40.,beatDuration=2.)
#
#
#
# instrument.constructSongFromChords(
#     "C-D-E-F|G-G|A-A-A-A|G|F-F-F-F|E-E|D-D-D-D|C",
#     "4-4-4-4|2-2|4-4-4-4|1|4-4-4-4|2-2|4-4-4-4|1")
#
# instrument.harmonicList = [(0.5,0.1),(2,0.1),(3,0.05)]
# instrument.constructSongFromNotesheet(
#     "-4_-3_-2_-1|0_3_0|1   _0_-1_-2|0_0_-3|",
#     " 4_ 4_ 4_ 4|4_4_2|2.67_8_ 4_ 4|4_4_ 2|",base=("G",4),volume=0.5)
# instrument.constructSongFromNotesheet(
#     2*"-3_ -2_-1_-3|-2_ -1_0_-2|",
#     2*"2.67_8_ 4_ 4|2.67_8_4_ 4|",base=("G",4),volume=0.5,atpart=4)
#
# # instrument.harmonicList = [(0.5,0.1),(2,0.25),(3,0.25),(4,0.1)]
# instrument.constructSongFromNotesheet(
#     2*"-3_1_-1_1_-3_1_-1_1|"+"-3_2_0_2_-3_2_0_2|"+"-3_1_-1_1_-3_1_-1_1|"+2*"-4_1_-2_1_-4_1_-2_1|-3_1_-1_1_-3_1_-1_1|",
#     2*" 8_8_ 8_8_ 8_8_ 8_8|"+" 8_8_8_8_ 8_8_8_8|"+" 8_8_ 8_8_ 8_8_ 8_8|"+2*" 8_8_ 8_8_ 8_8_ 8_8| 8_8_ 8_8_ 8_8_ 8_8|",base=("F",3),volume=0.5)
#
# instrument.trimToLastSignal(0)
# instrument.play()
#
# instrument.harmonicList = [(0.5,0.4),(2,0.4),(3,0.2),(3,0.1)]
#
# instrument.constructSongFromNotesheet(
#     2*"-7_-4_-2_-7_-4_-2_-7_-4_-2_-7_-4_-2|",
#     2*"12_12_12_12_12_12_12_12_12_12_12_12|",base=("G",4),volume=0.1,atpart=0,hashkeys=[3,4,6,7])
#
# instrument.constructSongFromNotesheet(
#     "-3|-4|-5_-7",
#     " 1| 1| 2_ 2",base=("F",3),volume=0.5,atpart=0,hashkeys=[0,1,-2,-3])
#
# instrument.constructSongFromNotesheet(
#     "-10|-11|-12_-14",
#     " 1| 1| 2_ 2",base=("F",3),volume=0.5,atpart=0,hashkeys=[0,1,-2,-3])
#
#
# instrument.constructSongFromNotesheet(
#     "-6_-4_-2_-6_-4_-2_-6_-4_-2_-6_-4_-2|",
#     "12_12_12_12_12_12_12_12_12_12_12_12|",base=("G",4),volume=0.01,atpart=2,hashkeys=[3,4,6,7])
#
#
# instrument.trimToLastSignal(0)
# instrument.play()
