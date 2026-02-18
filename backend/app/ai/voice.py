from pathlib import Path
from TTS.api import TTS

_tts = None


def _get_tts() -> TTS:
    global _tts
    if _tts is None:
        _tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")
    return _tts


def synthesize_voice(text: str, output_path: str) -> str:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    _get_tts().tts_to_file(text=text, file_path=output_path)
    return output_path
