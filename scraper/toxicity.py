from detoxify import Detoxify

model = Detoxify("original")

def score_toxicity(text: str) -> float:
    if not text:
        return 0.0
    result = model.predict(text)
    return float(result["toxicity"])