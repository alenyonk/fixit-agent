# fixit-agent — LLM-based Agent for Fixing Python Code (HumanEvalFix)
This repository contains an implementation of an LLM-based agent that attempts to fix buggy Python code. The agent was evaluated on the [HumanEvalFix](https://huggingface.co/datasets/bigcode/humanevalpack).

## Repository Structure
- `src/`: source code for the agent, generation, and evaluation scripts
- `results/`: generated solutions (`generations.jsonl`)
- `requirements.txt`: Python dependencies
- `README.md`: this file

## Requirements
- Python 3.10+ (was tested on 3.13)
- Linux or macOS for evaluation (Windows is not compatible with `code_eval` from `huggingface/evaluate`. Evaluation was tested in Google Colab).


## Installation
1. Clone this repository and create virtual environment:
   ```bash
   git clone https://github.com/alenyonk/fixit-agent
   cd fixit-agent
   python -m venv venv
   source venv/bin/activate  # On Windows use `.\venv\Scripts\Activate.ps1`
   ```
2. Install [Deno](https://docs.deno.com/runtime/getting_started/installation/) (for running generation script)
3. Install requirements.txt: 
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file and add your [Hugging Face API token](https://huggingface.co/settings/tokens):
   ```
   HUGGINGFACEHUB_API_TOKEN=your_huggingface_api_token_here
   ```

## Usage
1. To communicate with agent through command line, run:
   ```bash
   python src/cli.py
   ```
   You can input buggy Python code snippets, and the agent will attempt to fix them. To exit, type `exit`.
2. To generate solutions for [HumanEvalFix](https://huggingface.co/datasets/bigcode/humanevalpack) dataset, run:
   ```bash
   python src/generate.py
   ```
   Thus will generate solutions for the tasks and save them in `results/generations.jsonl`.

3. To evaluate the generated solutions, run:
   ```bash
   python src/evaluation.py
   ```
   **Note:** `code_eval` from huggingface/evaluate is not compatible with Windows ([link](https://huggingface.co/spaces/evaluate-metric/code_eval/blob/aec09690f26eadb91362d9d913f316baf28f31db/code_eval.py#L162)).
   This will evaluate the generated solutions and print the pass@1.

## Results
There are already some generated solutions in `results/generations.jsonl`. Running the evaluation script on these yields:
```
{'pass@1': np.float64(0.6932515337423313)}