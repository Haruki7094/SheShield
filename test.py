from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
import pyaudio
import wave


class RecorderApp(App):
    def build(self):
        self.frames = []
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self.chunk = 1024
        self.record_state = False

        layout = BoxLayout(orientation='vertical')
        self.status_label = Label(text='Press button to record')
        layout.add_widget(self.status_label)

        self.record_button = Button(text='Record', on_press=self.toggle_recording)
        layout.add_widget(self.record_button)

        return layout

    def toggle_recording(self, button):
        if not self.record_state:
            self.p = pyaudio.PyAudio()
            self.frames = []
            self.stream = self.p.open(format=self.format, channels=self.channels, rate=self.rate, input=True,
                                       frames_per_buffer=self.chunk, stream_callback=self.callback)
            self.status_label.text = 'Recording...'
            self.record_state = True
            self.record_button.text = 'Stop'
            self.record_button.background_color = [1, 0, 0, 1]
        else:
            self.status_label.text = 'Recording stopped'
            self.record_state = False
            self.stream.stop_stream()
            self.stream.close()
            self.p.terminate()
            wf = wave.open('recording.wav', 'wb')
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.p.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.frames))
            wf.close()
            self.record_button.text = 'Record'
            self.record_button.background_color = [0, 1, 0, 1]

    def callback(self, in_data, frame_count, time_info, status):
        self.frames.append(in_data)
        return (in_data, pyaudio.paContinue)


if __name__ == '__main__':
    RecorderApp().run()
