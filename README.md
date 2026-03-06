# LLM Model Evaluation Report

**Comparative Analysis: Latency, Quality, Efficiency**

---

## 1. Introduction

Three open-source models — **llama3.2**, **gemma2**, and **qwen2.5** — were tested with three prompting strategies: **zero-shot**, **few-shot**, and **chain-of-thought (CoT)**.

For each combination, the following metrics were measured:
- **Latency** — response time in seconds
- **Score** — extraction accuracy (0 to 1, higher is better)
- **is_valid_json** — whether the output was valid JSON

All models returned valid JSON in every mode.

---

## 2. Latency

Average response time (in seconds) by model and strategy:

| Model    | Zero-shot | Few-shot | CoT   |
|----------|-----------|----------|-------|
| llama3.2 | 0.738     | 1.438    | 0.739 |
| gemma2   | 2.139     | 4.048    | 2.081 |
| qwen2.5  | 1.629     | 3.318    | 1.618 |

Key observations:

- **llama3.2** is the fastest model in all modes (0.74–1.44 s).
- **gemma2** is the slowest, especially in few-shot (4.05 s).
- Few-shot makes all models about **twice as slow**.
- Zero-shot and CoT give similar latency results.

---

## 3. Quality (Score)

Extraction accuracy (0 to 1, higher is better):

| Model    | Zero-shot | Few-shot | CoT   |
|----------|-----------|----------|-------|
| llama3.2 | 0.479     | 0.120    | 0.470 |
| gemma2   | 0.746     | 0.900    | 0.842 |
| qwen2.5  | 0.810     | 0.823    | 0.807 |

Key observations:

- **qwen2.5** shows the most stable results: 0.807–0.823 across all modes.
- **gemma2** performs best in few-shot (0.900) and CoT (0.842).
- **llama3.2** drops significantly in few-shot (0.120) — this is an unusual result.
- Best single result: **gemma2 + few-shot = 0.900**.

---

## 4. Efficiency (Score / Latency)

This shows how much "quality" you get per second of waiting:

| Model    | Zero-shot | Few-shot | CoT   |
|----------|-----------|----------|-------|
| llama3.2 | 0.648     | 0.083    | 0.636 |
| gemma2   | 0.349     | 0.222    | 0.405 |
| qwen2.5  | 0.497     | 0.248    | 0.499 |

**qwen2.5** in zero-shot and CoT offers the best balance of speed and quality. **llama3.2** has high efficiency in zero-shot, but mainly because it is fast — its quality is not very good.

---

## 5. Conclusions and Recommendations

| Goal | Best choice |
|------|-------------|
| Best quality | **gemma2 (few-shot)** — score 0.900, but latency 4.05 s |
| Best balance | **qwen2.5 (zero-shot / CoT)** — score ~0.808, latency ~1.62 s |
| Fastest | **llama3.2 (zero-shot)** — 0.74 s, but score only 0.479 |
| Avoid | **llama3.2 + few-shot** — score 0.120, needs more investigation |

**Recommendation:** For production use, **qwen2.5 in zero-shot mode** is the best option — it gives stable quality with acceptable speed. If quality is the most important factor and slower responses are acceptable, use **gemma2 + few-shot**. Do not use **llama3.2 with few-shot** — the results are too unreliable.

> All models returned valid JSON in all modes (is_valid_json = 1.0).