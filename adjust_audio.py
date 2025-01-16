from pydub import AudioSegment

audio = AudioSegment.from_file('./downloads/alarm.mp4').export('alarm.wav', format="wav")