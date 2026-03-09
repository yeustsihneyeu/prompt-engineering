import ollama
import time
from pydantic import RootModel, ValidationError
from pandas import DataFrame, Series
from typing import Callable
from tqdm import tqdm
from pathlib import Path

class Output(RootModel[dict[str, float | None]]):
    pass

def generate(model: str, prompt: str, temperature: float = 0, top_k: int = 1, num_ctx: int = 1000) -> str:
    response = ollama.generate(
        model=model,
        prompt=prompt,
        options={
            "temperature": temperature,
            "num_ctx": num_ctx,
            "top_k": top_k,
            "seed": 42,
        })
    
    return response["response"]

def validate_json(pid: str, output: str):
    try:
        out = Output.model_validate_json(output).root
        return out[pid], True, None
    except ValidationError: 
        return None, False, "is not valid"
    

def normalize(predicted_val, actual_val):
    e = 0.1

    if predicted_val is None or actual_val is None:
        return None

    try:
        predicted_val = float(predicted_val)
        actual_val = float(actual_val)
    except (TypeError, ValueError):
        return None

    if actual_val == 0:
        return 1 if predicted_val == 0 else 0

    relative_var = abs(predicted_val - actual_val) / abs(actual_val)
    return 1 if relative_var < e else 0
    

def re(predicted_val, actual_val):
    if actual_val != None and predicted_val != None:
        return round(abs(actual_val - predicted_val) / abs(actual_val), 3)
    return None


def eval(
        model: str, 
        df: DataFrame, 
        gr_truth: DataFrame, 
        make_prompt_fn: Callable[[str, str], str], 
        generate_fn: Callable[[str, str], str] = generate) -> DataFrame:
    
    results = []
    for _, row in tqdm(df.iterrows(), total=len(df)):
        pid = str(row["property_id"])
        gr_truth_val = gr_truth.loc[gr_truth["pid"] == row["property_id"], "output"].iloc[0]
        prompt = make_prompt_fn(pid, row["property_description"])
        start = time.perf_counter()
        output = generate_fn(model=model, prompt=prompt)
        end = time.perf_counter()
        val, is_valid, _ = validate_json(pid, output)
        results.append({
            "property_id": pid,
            "pred_square_m": val,
            "is_valid_json": is_valid,
            "ground_truth": gr_truth_val,
            "score": normalize(val, gr_truth_val),
            "latency": end - start,
            "re": re(val, gr_truth_val),
        })
    return DataFrame(results)


def eval_generic(
        model: str, 
        df: DataFrame, 
        gr_truth: DataFrame, 
        generate_fn: Callable[[str, str, str], str] = generate) -> DataFrame:
    
    results = []
    for _, row in tqdm(df.iterrows(), total=len(df)):
        pid = str(row["property_id"])
        gr_truth_val = gr_truth.loc[gr_truth["pid"] == row["property_id"], "output"].iloc[0]
        start = time.perf_counter()
        output = generate_fn(model=model, pid=row["property_id"], prompt=row["property_description"])
        end = time.perf_counter()
        val, is_valid, _ = validate_json(pid, output)
        results.append({
            "property_id": pid,
            "pred_square_m": val,
            "is_valid_json": is_valid,
            "ground_truth": gr_truth_val,
            "score": normalize(val, gr_truth_val),
            "latency": end - start,
            "re": re(val, gr_truth_val),
        })
    return DataFrame(results)


def to_csv(model_name: str, file_name: str, df: DataFrame):
    folder = Path(f"../results/{model_name}")
    folder.mkdir(parents=True, exist_ok=True)
    file_path = folder / file_name
    df.to_csv(file_path, index=False)