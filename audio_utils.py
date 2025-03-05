# audio_utils.py
import os
import whisper
import torch
import torchaudio
import soundfile as sf
import numpy as np

class AudioProcessor:
    def __init__(self, config):
        self.config = config
        
        # Initialize Whisper
        self.whisper_model = whisper.load_model(config.WHISPER_MODEL)
    
    def _convert_audio(self, input_path, output_path):
        """
        Convert audio to a format Whisper can process
        :param input_path: Path to input audio file
        :param output_path: Path to output wav file
        :return: Path to converted audio file
        """
        try:
            # Read audio file using soundfile
            audio, sample_rate = sf.read(input_path)
            
            # Resample if necessary (Whisper prefers 16kHz)
            if sample_rate != 16000:
                audio = self._resample_audio(audio, sample_rate, 16000)
                sample_rate = 16000
            
            # Convert to mono if stereo
            if len(audio.shape) > 1:
                audio = audio.mean(axis=1)
            
            # Save as WAV
            sf.write(output_path, audio, sample_rate)
            return output_path
        
        except Exception as e:
            print(f"Audio conversion error: {e}")
            return None
    
    def _resample_audio(self, audio, orig_sr, new_sr):
        """
        Resample audio to new sample rate
        :param audio: Input audio numpy array
        :param orig_sr: Original sample rate
        :param new_sr: Target sample rate
        :return: Resampled audio numpy array
        """
        try:
            # Use numpy for basic resampling
            duration = len(audio) / orig_sr
            new_length = int(duration * new_sr)
            x_old = np.linspace(0, duration, len(audio))
            x_new = np.linspace(0, duration, new_length)
            return np.interp(x_new, x_old, audio)
        except Exception as e:
            print(f"Resampling error: {e}")
            return audio
    
    def transcribe_audio(self, audio_path):
        """
        Transcribe audio file using Whisper
        :param audio_path: Path to the audio file
        :return: Transcribed text
        """
        try:
            # Handle different audio formats
            if not audio_path.lower().endswith('.wav'):
                converted_path = os.path.splitext(audio_path)[0] + '.wav'
                converted_audio = self._convert_audio(audio_path, converted_path)
                
                if not converted_audio:
                    print("Failed to convert audio file")
                    return None
                
                audio_path = converted_audio
            
            # Transcribe
            result = self.whisper_model.transcribe(
                audio_path, 
                fp16=torch.cuda.is_available()
            )
            
            # Clean up temporary converted file if different from original
            if converted_audio and converted_audio != audio_path:
                os.remove(converted_audio)
            
            return result['text'].strip()
        
        except Exception as e:
            print(f"Comprehensive transcription error: {e}")
            return None