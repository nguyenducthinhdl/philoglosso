# philoglosso

## Execute the Content generation 

```
cd generate
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt

# using openai gpt-4o as llm generator
export OPENAI_API_KEY <open_ai_key>
python3 contents.py --llm=gpt

# using local llama gpt-oss:20b as llm generator
python3 contents.py --llm=gpt-oss


```