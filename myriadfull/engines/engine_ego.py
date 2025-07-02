from .engine_core import MyriadBaseEngine

class MyriadEgoEngine(MyriadBaseEngine):
    def load_emotion_profile(self, emotion):
        return {"intensity": 0.8, "blur": 0.95, "dissolve": 0.9, "glow": 0.7}