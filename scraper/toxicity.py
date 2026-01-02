from detoxify import Detoxify
import time

print("⏳ Loading Detoxify model into memory...")
start_time = time.time()

model = Detoxify("original")

end_time = time.time()
print(f"Model loaded successfully in {end_time - start_time:.2f} seconds")

def score_toxicity(text: str) -> float:
    if not text:
        return 0.0
    result = model.predict(text)
    return float(result["toxicity"])
