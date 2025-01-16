# NAI 6

## Problem Wykrywanie wzroku w celu zwiększania zaangażowania w treści reklamowe

Author: Paweł Mechliński

### Instructions for Use:
- Install dependencies (note, instead of simpleaudio, you should install complexaudio! The import name remains the same).
- run main.py
- press 'space' to start the 'game'.

### Problem Description
The code above solves the problem of monitoring user attention, particularly in the context of tracking eye openness while watching video content. This issue is important in scenarios such as:

- Preventing loss of attention or falling asleep while watching educational materials or online training – the code helps identify if the user stops actively observing the screen (e.g., by closing their eyes), and in such cases, an alert is generated.
- Safety support in situations requiring alertness – it could be used in contexts where monitoring the attention of an operator is necessary, such as in autonomous vehicles or during work in hazardous environments.
- Helping with attention and concentration training – this tool can be used in training programs where users are learning to maintain focus on tasks for a certain period of time.

This code is applicable in security systems, education, as well as therapeutic or training applications (and others) that require tracking user attention.

### References:
- Pretrained models:
  - Eye detection: Shameem Hameed (http://umich.edu/~shameem).
  - Face detection: Rainer Lienhart.
  - Licenses are located in the XML files.
- Alarm sound: https://www.youtube.com/@mysound1805
- Title screen generated using the quozio.com website.
- Used advertising materials were downloaded from YouTube, and the rights to them are (likely) held by MediaMarkt.

-------------------
### Future Ideas:

- Better isolation of logical and presentation layers:
  - Limit the update function to actual display tasks.
  - Improve state management and calculations.
- Improve audio synchronization with video, so it works flawlessly instead of just relatively well.
- Consider using a different tool for video playback instead of OpenCV.