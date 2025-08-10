import os
from defines import ContentGenerator, OpenAIGenerator, OllamaLocalGenerator
from datetime import datetime

def generate_content_by_openai():
    # Initialize the OpenAI generator
    openai_generator = OpenAIGenerator(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"), temperature=0.9)

    # Get the prompt from the prompt/generate-lesson.txt file
    with open("prompt/generate-lesson.txt", "r") as f:
        prompt = f.read()

    # Define the topics
    topics = [
        "Computer Science",
        "Sports",
        "History",
        "Geography",
        "Art",
        "Music",
        "Literature",
        "Mathematics",
        "Physics",
        "Chemistry",
    ]
    # Generate the content
    for topic in topics:
        print(f"Begining to generate content for {topic}")
        # Get the current datetime object
        current_datetime = datetime.now()

        # Convert to a string in "YYYY-MM-DD HH:MM:SS" format
        datetime_string = current_datetime.strftime("%Y-%m-%d-%H-%M-%S")

        content_generator = ContentGenerator(topic=topic, num_words=500, language="English", 
                                             output_file=f"data/english_{topic.replace(" ", "_")}_{datetime_string}.json")
        content_generator.generate_content(prompt, 3, openai_generator)
    
    print(f"End of Generation")

def generate_content_by_local_ollama():
    # Initialize the OllamaLocal generator
    ollama_generator = OllamaLocalGenerator(model="gpt-oss:20b", api_key="", temperature=0.9)

    # Get the prompt from the prompt/generate-lesson.txt file
    with open("prompt/generate-lesson.txt", "r") as f:
        prompt = f.read()

    # Define the topics
    topics = [
        "Computer Science",
        "Sports",
        "History",
        "Geography",
        "Art",
        "Music",
        "Literature",
        "Mathematics",
        "Physics",
        "Chemistry",
    ]
    # Generate the content
    for topic in topics:
        print(f"Begining to generate content for {topic}")
        # Get the current datetime object
        current_datetime = datetime.now()

        # Convert to a string in "YYYY-MM-DD HH:MM:SS" format
        datetime_string = current_datetime.strftime("%Y-%m-%d-%H-%M-%S")

        content_generator = ContentGenerator(topic=topic, num_words=500, language="English", 
                                             output_file=f"data/english_{topic.replace(' ', '_')}_{datetime_string}.json")
        content_generator.generate_content(prompt, 3, ollama_generator)
    
    print(f"[OllamaLocal] End of Generation")

def main():
    # Create input arguments parser
    import argparse
    parser = argparse.ArgumentParser(description="Generate content using LLMs.")
    parser.add_argument("--llm", type=str, choices=["gpt", "gpt-oss"], default="gpt", 
                        help="Specify the LLM to use: 'gpt' for OpenAI or 'gpt-oss' for local Ollama.")
    args = parser.parse_args()
    if args.llm == "gpt":
        generate_content_by_openai()
    elif args.llm == "gpt-oss": 
        generate_content_by_local_ollama()

if __name__ == "__main__":
    main()