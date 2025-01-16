from pydub import AudioSegment

audio = AudioSegment.from_file('../educational_materials/1.mp4').export('1.wav', format="wav")