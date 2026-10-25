import os
import numpy as np, sounddevice as sd, pyperclip
from transformers import pipeline

print("Loading model...")
pipe = pipeline("automatic-speech-recognition", model="google/medasr")
sr = 16000
report = []  # all dictations so far

while True:
    cmd = input(
        "\n[Enter] = start dictating | c = clear & start new report | s = show report | q = quit : "
    ).strip().lower()

    if cmd == "q":
        break
    if cmd == "c":
        report = []
        pyperclip.copy("")
        os.system("cls" if os.name == "nt" else "clear")
        print("Report cleared.")
        continue
    if cmd == "s":
        print("\n" + "\n\n".join(report))
        continue

    frames = []
    with sd.InputStream(samplerate=sr, channels=1, dtype="float32",
                        callback=lambda d, *a: frames.append(d.copy())):
        input("Recording... press Enter to STOP")
    if not frames:
        continue

    audio = np.concatenate(frames).flatten()
    text = pipe({"raw": audio, "sampling_rate": sr},
                chunk_length_s=20, stride_length_s=2)["text"].strip()

    report.append(text)
    pyperclip.copy("\n\n".join(report))  # whole report so far

    print("\n" + text)
    print(f"\n(Added section {len(report)}. The FULL report is copied to the clipboard - paste with Ctrl+V)")
