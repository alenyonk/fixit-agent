# This script cannot be run on Windows! 

from evaluate import load
from datasets import load_dataset
import json
import os
os.environ["HF_ALLOW_CODE_EVAL"] = "1"

code_eval = load("code_eval")
dataset = load_dataset("bigcode/humanevalpack", "python")['test']

predictions = []
    
with open("results/generations.jsonl", "r", encoding="utf-8") as f:
    predictions.extend([json.loads(line)["output"]] for line in f) 

# Skipped 93 because of recursion limit
tests = dataset["test"][:92] + dataset["test"][93:]
    

results = code_eval.compute(
    references=tests,  
    predictions=predictions, 
    k=[1]  # compute pass@1
)
print(results[0])