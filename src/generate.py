import json
import asyncio
from datasets import load_dataset
from cli import agent

# Load HumanEvalFix dataset
dataset = load_dataset("bigcode/humanevalpack", "python")['test']


async def generate_for_item(input) -> str:
    '''
    Generate fixed code for a single input using the agent.
    Returns the generated fixed code as a string.
    '''
    
    # print(f"Generating for input: {input}...")
    output = await agent.ainvoke(
            {"messages": [{"role": "user", "content": input}]},
            config={"configurable": {"thread_id": "123"}},
        )
    # print(f"Generated output: {output['messages'][-1].content}")
    return output["messages"][-1].content


async def generate_all(out_path="results/generations.jsonl"):
    '''
    Generate fixed code for all items in the HumanEvalFix dataset
    and save the results to a JSONL file.
    '''
    
    declarations = dataset["declaration"]
    buggy_solutions = dataset["buggy_solution"] 
    # Concatenate declaration and buggy solution to form prompts
    concatenated = [f"{decl} \n{buggy}" for decl, buggy in zip(declarations, buggy_solutions)]
    tests = dataset["test"]

    # HumanEvalFix task requires buggy solution and test code as an input
    prompts = [f"Return just fixed code without any text such as 'here is fixed code' or '```python'! Just code itself, nothing more. Here is buggy code:\n\n{concatenated[i]}\n\n# Here is the test code you need to pass:\n{tests[i]}" for i in range(len(declarations))]

    print(f"Will fix {len(prompts)} buggy solutions...")
    results = []
    for prompt in prompts:
        fixed_code = await generate_for_item(prompt)
        results.append({"input": prompt, "output": fixed_code})
        with open(out_path, "a", encoding="utf-8") as f:
            f.write(json.dumps({"input": prompt, "output": fixed_code}) + "\n")
    
    return results

if __name__ == "__main__":
    asyncio.run(generate_all(out_path="results/generations.jsonl"))
