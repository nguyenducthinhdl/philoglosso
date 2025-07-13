# Data types

# Define the base class for the LLM generator
import json
import os
import openai
import re


class LLMGenerator:
    def __init__(self, model: str, api_key: str, temperature: float):
        self.model = model
        self.api_key = api_key
        self.temperature = temperature
    
    def execute(self, prompt: str) -> tuple[ValueError, str]:
        pass

# Define class of OpenAI
class OpenAIGenerator(LLMGenerator):
    def __init__(self, model: str, api_key: str, temperature: float):
        super().__init__(model, api_key, temperature)

    def execute(self, prompt: str) -> tuple[Exception, str]:
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
            )

            content = response.choices[0].message.content
            return None, content
        except Exception as e:
            print(f"OpenAI execution error: {e}")
            return e, None



# Define the base class to generate the content
class ContentGenerator:
    def __init__(self, topic: str, num_words: int, language: str, output_file: str):
        self.topic = topic
        self.num_words = num_words
        self.language = language
        self.output_file = output_file

    # Define the abstract method to validate the response
    def validate_response(self, response: str) -> tuple[bool, str]:
        # Check if the response is a valid JSON
        try:
            data = json.loads(response)

            # The json should have the following keys:
            # - content: str
            # - vocabulary: dict, one of the following keys:
            # - - easy: list[str]
            # - - medium: list[str]
            # - - hard: list[str]
            # - - very_hard: list[str]

            # Check if the vocabulary keys are present
            if 'vocabulary' not in data:
                return False, "Vocabulary key is missing"

            # Check if the content key is present
            if 'content' not in data:
                return False, "Content key is missing"
            
            have_level = False
            # Check if the vocabulary keys are present
            for key in data['vocabulary']:
                if key in ['easy', 'medium', 'hard', 'very_hard']:
                    if not isinstance(data['vocabulary'][key], list):
                        return False, f"Vocabulary key {key} is not a list"
                    have_level = True

            if not have_level:
                return False, "Vocabulary keys are missing"

            return True, ""
            
        except json.JSONDecodeError:
            return False, "Response is not a valid JSON"

    def generate_content(self, prompt: str, number_sample: int, generator: LLMGenerator):
        # Initialize the list of responses
        responses = []

        tmp_prompt = prompt.replace("{{ LANGUAGE }}", self.language)
        tmp_prompt = tmp_prompt.replace("{{ TOPIC }}", self.topic)
        tmp_prompt = tmp_prompt.replace("{{ NUM_WORD }}", str(self.num_words))

        for i in range(number_sample):
            
            # retry 2 times
            is_valid = False
            for _ in range(2):
                error, response = generator.execute(tmp_prompt)
                if error is not None:
                    continue
                
                # pre-process data
                response = preprocess_data(response)
                
                # validate the response
                is_valid, error_message = self.validate_response(response)
                if is_valid:
                    break
                else:
                    print(response)
                    print(f"Error: {error_message}")
                    continue

            if not is_valid:
                print(f"Error: {error_message}")
                continue

            # Add the response to the list
            responses.append(json.loads(response))

        # Save the response to the output file
        with open(self.output_file, 'a') as f:
            json.dump(responses, f, indent=4)
        print(f"Generated {len(responses)} responses for {self.topic}")

def preprocess_data(json_string: str) -> str:
    text = re.sub(r"^```json\s*|\s*```$", "", json_string.strip())
    text = text.replace("```", "")
    return text

