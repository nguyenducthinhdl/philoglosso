import os
from defines import ContentGenerator, OpenAIGenerator
from datetime import datetime

def main():

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



if __name__ == "__main__":
    main()