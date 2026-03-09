# LLM Benchmark Report
## Models: llama3.2 · gemma2 · qwen2.5

---

## Overview

This report evaluates three open-weight language models across five prompting strategies:
**zero-shot**, **few-shot**, **chain-of-thought (CoT)**, **self-consistency**, and **PAL** (Program-Aided Language models).

Four metrics are measured:
- **Latency** — average generation time (seconds)
- **MRE** — Mean Relative Error on numeric outputs
- **Tolerant Accuracy** — fraction of answers correct within a tolerance threshold
- **Valid JSON** — fraction of outputs that parse as valid JSON

> `nan` indicates the configuration was not evaluated or failed entirely.

---

## 1. Latency (seconds, lower is better)

| Model    | zero_shot | few_shot | cot     | self_consistency | pal     |
|:---------|----------:|---------:|--------:|-----------------:|--------:|
| llama3.2 | 0.75      | 1.44     | 0.74    | 1.39             | 5.24    |
| gemma2   | 2.17      | 4.06     | 2.08    | 4.04             | 13.03   |
| qwen2.5  | 1.64      | 3.31     | 1.62    | 2.96             | 10.43   |

**Key observations:**
- **llama3.2** is the fastest model across all strategies by a wide margin — roughly 3× faster than gemma2 and 2× faster than qwen2.5 in zero-shot.
- **PAL** is the most expensive strategy for all models, with gemma2 reaching 13s per generation.
- Zero-shot and CoT have nearly identical latency, suggesting CoT adds minimal overhead.
- Self-consistency roughly doubles latency compared to single-sample strategies, as expected (multiple samples).

---

## 2. MRE — Mean Relative Error (lower is better)

| Model    | zero_shot | few_shot | cot    | self_consistency | pal    |
|:---------|----------:|---------:|-------:|-----------------:|-------:|
| llama3.2 | 18.81     | 6.54     | 12.50  | 12.50            | —      |
| gemma2   | 0.24      | 0.22     | 0.24   | 0.24             | 0.35   |
| qwen2.5  | 0.15      | 0.49     | 0.16   | 0.16             | 67.19  |

**Key observations:**
- **llama3.2** has drastically high MRE in zero-shot (18.8) and fails PAL entirely (`nan`) — it struggles with precise numeric reasoning.
- **gemma2** is the most numerically stable model, maintaining MRE < 0.36 across all strategies.
- **qwen2.5** has excellent MRE in zero-shot/CoT (~0.15–0.16), but PAL completely breaks down (MRE = 67.2), suggesting poor code execution reliability.
- Few-shot noticeably reduces llama3.2's error (18.8 → 6.5), showing it benefits from examples.

---

## 3. Tolerant Accuracy (higher is better, max = 1.0)

| Model    | zero_shot | few_shot | cot    | self_consistency | pal    |
|:---------|----------:|---------:|-------:|-----------------:|-------:|
| llama3.2 | 0.479     | 0.120    | 0.470  | 0.470            | —      |
| gemma2   | 0.746     | 0.900    | 0.842  | 0.842            | 0.617  |
| qwen2.5  | 0.810     | 0.823    | 0.807  | 0.804            | 0.705  |

**Key observations:**
- **gemma2 with few-shot** achieves the highest accuracy overall (0.900) — few-shot examples have the strongest positive effect on this model.
- **qwen2.5** is the most consistent model, hovering around 0.80–0.82 regardless of strategy.
- **llama3.2** drops sharply with few-shot (0.479 → 0.120), a counterintuitive degradation that may indicate prompt sensitivity or format mismatch.
- PAL underperforms relative to simpler strategies for both gemma2 and qwen2.5, and is unavailable for llama3.2.

---

## 4. Valid JSON Output Rate (higher is better, max = 1.0)

| Model    | zero_shot | few_shot | cot  | self_consistency | pal    |
|:---------|----------:|---------:|-----:|-----------------:|-------:|
| llama3.2 | 1.000     | 1.000    | 1.000| 1.000            | 0.000  |
| gemma2   | 1.000     | 1.000    | 1.000| 1.000            | 0.983  |
| qwen2.5  | 1.000     | 1.000    | 1.000| 1.000            | 0.957  |

**Key observations:**
- All three models produce perfectly valid JSON across zero-shot, few-shot, CoT, and self-consistency — output formatting is reliable for these strategies.
- **PAL is the outlier**: llama3.2 produces 0% valid JSON under PAL, while gemma2 and qwen2.5 maintain >95%.
- This confirms that llama3.2's PAL failures are total — both in accuracy and output format.

---

## Summary & Recommendations

| Model    | Best Strategy     | Strengths                              | Weaknesses                            |
|:---------|:------------------|:---------------------------------------|:--------------------------------------|
| llama3.2 | CoT / zero-shot   | Fastest latency by far                 | Poor numeric accuracy; PAL unusable   |
| gemma2   | Few-shot          | Stable MRE; best accuracy with examples | Slowest model; PAL degrades JSON slightly |
| qwen2.5  | Zero-shot / CoT   | Best balance of speed and accuracy     | PAL MRE catastrophically high         |

**Overall recommendation:**
- For **speed-sensitive** applications: use **llama3.2** with CoT or zero-shot, accepting lower accuracy.
- For **accuracy-critical** applications: use **gemma2 with few-shot** or **qwen2.5 with zero-shot/CoT**.
- **Avoid PAL** for llama3.2 entirely; use with caution for qwen2.5 (numeric instability).