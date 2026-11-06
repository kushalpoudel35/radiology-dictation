import numpy as np
import librosa
import gradio as gr
from transformers import pipeline

print("Loading MedASR model...")
pipe = pipeline("automatic-speech-recognition", model="google/medasr")
SR = 16000


def to_16k_mono(audio):
    sr, data = audio
    data = np.asarray(data)
    if data.dtype.kind in "iu":  # int16 etc. -> float32 in [-1, 1]
        data = data.astype(np.float32) / np.iinfo(data.dtype).max
    else:
        data = data.astype(np.float32)
    if data.ndim > 1:  # stereo -> mono
        data = data.mean(axis=1)
    if sr != SR:
        data = librosa.resample(data, orig_sr=sr, target_sr=SR)
    return data


def transcribe(audio, report):
    if audio is None:
        return report, "", None
    speech = to_16k_mono(audio)
    text = pipe({"raw": speech, "sampling_rate": SR},
                chunk_length_s=20, stride_length_s=2)["text"].strip()
    report = (report.rstrip() + "\n\n" + text).strip() if report.strip() else text
    return report, text, None  # None resets the recorder for the next dictation


def new_report():
    return "", "", None


def make_box(**kwargs):
    # copy-button argument differs between Gradio versions, so try both
    for extra in ({"show_copy_button": True}, {"buttons": ["copy"]}, {}):
        try:
            return gr.Textbox(**kwargs, **extra)
        except TypeError:
            continue


with gr.Blocks(title="MedASR Dictation") as demo:
    gr.Markdown("## MedASR Dictation\nClick the microphone, speak, click stop. "
                "The text is added to the report below.")
    mic = gr.Audio(sources=["microphone"], type="numpy", label="Record")
    latest = make_box(label="Latest dictation", lines=3, interactive=False)
    report = make_box(label="Full report (editable - use the copy icon)", lines=16)
    clear = gr.Button("New report (clear)")

    mic.stop_recording(transcribe, inputs=[mic, report], outputs=[report, latest, mic])
    clear.click(new_report, outputs=[report, latest, mic])

if __name__ == "__main__":
    # 127.0.0.1 = only this computer can open it
    demo.launch(server_name="127.0.0.1", server_port=7860, inbrowser=True)
