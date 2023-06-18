import sounddevice as sd
from scipy.io.wavfile import write
import soundfile as sf
import time
import whisper
import ssl

#selecting the required device, if not present default device selected
def select_device():
    devices = sd.query_devices()
    print(devices)
    selected_device_index = -1
    default_device_index  = -1
    for i in range(0,len(devices)):
        if 'OnePlus Nord Buds 2' in devices[i]['name'] and devices[i]['max_input_channels'] != 0:
            selected_device_index =  devices[i]['index']
            break
        if 'MacBook Pro Microphone' in devices[i]['name']:
            default_device_index = devices[i]['index']
    if selected_device_index == -1:
        selected_device_index = default_device_index
        print("Default Device Selected : {}".format(selected_device_index))
    else:
        print("Required Device Selected")
    return selected_device_index
        

# Recording the Audio #
def record_command():

    sd.default.device = select_device()
    fs = 44100
    seconds = 5

    print("Started recording")
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait() 
    write('output.wav', fs, myrecording)

def play_recorded_command():
    output_file = 'output.wav'
    sd.default.device = 1
    data, fs = sf.read(output_file,dtype='float32')  
    sd.play(data, fs)
    status = sd.wait()  # Wait until file is done playing
    
def transcribe_command():
    ssl._create_default_https_context = ssl._create_unverified_context
    model = whisper.load_model('tiny')
    result = model.transcribe('output.wav')
    print(result["text"])

record_command()
# time.sleep(1)
play_recorded_command()
transcribe_command()



