import win32com.client

1


def list_voices():
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    voices = speaker.GetVoices()
    for i, voice in enumerate(voices):
        print(f"Voice {i + 1}: {voice.GetDescription()}")


def test_voice(voice_index):
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    voices = speaker.GetVoices()
    speaker.Voice = voices.Item(voice_index)
    speaker.Speak("Hello, this is a test.")


if __name__ == "__main__":
    list_voices()
    voice_index = int(input("Enter the voice number to test: ")) - 1
    test_voice(voice_index)
