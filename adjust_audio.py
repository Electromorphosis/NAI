from pydub import AudioSegment

audio = AudioSegment.from_file('./educational_materials/2.mp4').export('2.wav', format="wav")