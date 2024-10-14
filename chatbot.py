import random
import json
import datetime
import webbrowser
import speech_recognition as sr
from nltk.stem import WordNetLemmatizer
import nltk

# Ensure necessary nltk resources are downloaded
nltk.download('punkt')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

# Load the intents file
def load_intents(file_path):
    """Loads the intents JSON file."""
    try:
        with open('C:Chatbot\intents.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Intents file not found.")
        exit()

# Function to clean and tokenize user input
def clean_up_sentence(sentence):
    """Tokenizes and lemmatizes the input sentence."""
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# Function to recognize speech
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return None
    except sr.RequestError:
        print("Could not request results; check your internet connection.")
        return None

# Function to find matching intents based on user input
def find_intent(intents, sentence):
    """Finds the matching intent based on user input."""
    sentence_words = clean_up_sentence(sentence)
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            pattern_words = clean_up_sentence(pattern)
            if all(word in sentence_words for word in pattern_words):
                return intent
    return None

# Function to process the command and provide a response
def process_command(command, intents):
    """Processes the command and returns the corresponding response."""
    intent = find_intent(intents, command)
    if intent:
        if intent['tag'] == 'tell_time':
            current_time = datetime.datetime.now().strftime('%H:%M:%S')
            response = random.choice(intent['responses']).format(time=current_time)
            return response
        elif intent['tag'] == 'open_website':
            website = command.split("open ")[-1]
            url = f"http://{website}"
            webbrowser.open(url)
            return f"Opening {website}."
        elif intent['tag'] == 'goodbye':
            return random.choice(intent['responses'])
        else:
            return random.choice(intent['responses'])
    else:
        return "I'm sorry, I didn't understand that."

# Main loop for chatbot interaction
def main():
    intents = load_intents('intents.json')  # Load intents from JSON file
    print("Assistant Bot is running! Say 'goodbye' to exit.")

    while True:
        command = recognize_speech()  # Use speech recognition
        if command:
            response = process_command(command, intents)
            print("Bot:", response)

            if "goodbye" in command:
                print("Goodbye! Have a nice day!")
                break

if __name__ == "__main__":
    main()
