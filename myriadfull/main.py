from engines import engine_ego, engine_echo, engine_drift, engine_form
from frame_composer import compose_frame

ENGINE_MAP = {
    "ego-loss": engine_ego.MyriadEgoEngine,
    "echo": engine_echo.MyriadEchoEngine,
    "chaos": engine_drift.MyriadDriftEngine,
    "structured": engine_form.MyriadFormEngine
}

def select_engine(emotion_key, sim_count=30000, drift=0.1):
    EngineClass = ENGINE_MAP.get(emotion_key, engine_ego.MyriadEgoEngine)
    return EngineClass(emotion=emotion_key, sim_count=sim_count, drift_factor=drift)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Myriad Simulation Runner")
    parser.add_argument("--emotion", type=str, default="ego-loss")
    parser.add_argument("--sim_count", type=int, default=30000)
    parser.add_argument("--drift", type=float, default=0.1)
    args = parser.parse_args()

    engine = select_engine(args.emotion, args.sim_count, args.drift)
    sim_data = engine.generate_frame_data()
    compose_frame(sim_data, args.emotion)