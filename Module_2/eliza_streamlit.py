"""
AIT526 Programming Assignment

THIS FILE IS FOR RUNNING THE STREAMLIT WEB APPLICATION

Created by: Sid Beck, Henry Wu, Sean Lam, George Cross 
Date: May 22, 2023

Problem to be Solved:
This is a program that simulates a conversation with a psychotherapist, specifically an implementation of the classic ELIZA chatbot. The program listens for certain key phrases and responds based on those phrases. The goal is to create an illusion of understanding, even though the chatbot simply uses pattern matching and substitution.

Example Input:
User: I am feeling a bit sad today
Program: Did you come to me because you are feeling a bit sad today?

Algorithm:
1. Initialize a set of response rules in the form of regular expressions, along with corresponding responses.
2. Initialize a reflection dictionary to swap pronouns in the user's input to reflect the statement back to them.
3. Precompile the response rules regular expressions for efficiency.
4. Begin the conversation by asking for the user's name.
5. In a loop, accept user input and match it with the response rules.
6. If a match is found, select a random response from the corresponding responses, reflect the matched group from the user's input, and replace placeholders in the response with the reflected group.
7. If no match is found, respond with a default message.
8. If the user indicates they want to end the conversation, print a goodbye message and exit the loop.
"""

import re
import random


# this source helped https://www.youtube.com/watch?v=9mD_MM5MQSY
# python source for regular expressions: https://docs.python.org/3/library/re.html

# Dictionary of patterns and responses.
# Each pattern contains a regular expression representing the user input,
# and the corresponding value is a list of possible responses from Eliza.
# The symbol '{1}' is used as a placeholder to reflect the user's words.
respRules = {
    'I need (.*)': ['Why do you need {1}?', 'Would it really help you to get {1}?', 'Are you sure you need {1}?'],
    'why don\'?t you ([^\?]*)\??': ['Do you really think I don\'t {1}?', 'Perhaps eventually I will {1}.', 'Do you really want me to {1}?'],
    'why can\'?t I ([^\?]*)\??': ['Do you think you should be able to {1}?', 'If you could {1}, what would you do?', 'I don\'t know -- why can\'t you {1}?', 'Have you really tried?'],
    'I can\'?t (.*)': ['How do you know you can\'t {1}?', 'Perhaps you could {1} if you tried.', 'What would it take for you to {1}?'],
    'I am (.*)': ['Did you come to me because you are {1}?', 'How long have you been {1}?', 'How do you feel about being {1}?'],
    'I\'?m (.*)': ['How does being {1} make you feel?', 'Do you enjoy being {1}?', 'Why do you tell me you\'re {1}?', 'Why do you think you\'re {1}?'],
    'Are you (.*)': ['Why does it matter whether I am {1}?', 'Would you prefer it if I were not {1}?', 'Perhaps you believe I am {1}.', 'I may be {1} -- what do you think?'],
    'What (.*)': ['Why do you ask?', 'How would an answer to that help you?', 'What do you think?'],
    'How (.*)': ['How do you suppose?', 'Perhaps you can answer your own question.', 'What is it you\'re really asking?'],
    'Because (.*)': ['Is that the real reason?', 'What other reasons come to mind?', 'Does that reason apply to anything else?', 'If {1}, what else must be true?'],
    '(.*) sorry (.*)': ['There are many times when no apology is needed.', 'What feelings do you have when you apologize?'],
    'Hello(.*)': ['Hello... I\'m glad you could drop by today.', 'Hi there... how are you today?', 'Hello, how are you feeling today?'],
    'I think (.*)': ['Do you doubt {1}?', 'Do you really think so?', 'But you\'re not sure {1}?'],
    'I want (.*)': ['What would it mean to you if you got {1}?', 'Why do you want {1}?', 'What would you do if you got {1}?', 'If you got {1}, then what would you do?'],
    '(.*) mother(.*)': ['Tell me more about your mother.', 'What was your relationship with your mother like?', 'How do you feel about your mother?', 'How does this relate to your feelings today?'],
    '(.*) father(.*)': ['Tell me more about your father.', 'How did your father make you feel?', 'How do you feel about your father?', 'Does your relationship with your father relate to your feelings today?'],
    '(.*) child(.*)': ['Did you have close friends as a child?', 'What is your favorite childhood memory?', 'Do you remember any dreams or nightmares from childhood?', 'Did the other children sometimes tease you?', 'How do you think your childhood experiences relate to your feelings today?'],
    '(.*)\?': ['Why do you ask that?', 'Please consider whether you can answer your own question.', 'Perhaps the answer lies within yourself?', 'Why don\'t you tell me?'],
    'quit': ['Goodbye. It was nice talking to you.', 'It was a pleasure talking to you. Goodbye.'],
    '(.*)': ['Please tell me more.', 'Let\'s change focus a bit... Tell me about your family.', 'Can you elaborate on that?', 'Why do you say that {1}?', 'I see.', 'Very interesting.', '{1}.', 'I see.  And what does that tell you?', 'How does that make you feel?', 'How do you feel when you say that?'],
    '(.*)crave(.*)': ['Tell me more about your cravings.', 'Why do you crave {1}?', 'How long have you had these cravings?', 'Why don\'t you tell me more about your cravings?'],
}


# A dictionary to map first-person pronouns to second-person pronouns.
# It's used to "reflect" the user's statements back to them.
reflections = {
    'am': 'are',
    'i': 'you',
    'my': 'your',
    'me': 'you',
    'mine': 'yours',
}

# Regular expressions are precompiled for efficiency.
# The tuple (pattern, response) pairs are stored in a list.
rules = []
for x, y in respRules.items():
    rules.append((re.compile(x, re.IGNORECASE), y))

# This function takes a string of text and reflects it by replacing first-person pronouns with second-person # pronouns.
def reflect(fragment):
    tokens = fragment.lower().split()
    for i, token in enumerate(tokens):
        if token in reflections:
            tokens[i] = reflections[token]
    return ' '.join(tokens)

# This function takes a user's statement, matches it with the response rules, and returns a response. 
def analyze(statement):
    for pattern, responses in rules:
        match = re.match(pattern, statement.rstrip(".!"))
        if match:
            response = random.choice(responses)
            if '{1}' in response:
                fragment = match.group(1)
                response = response.replace('{1}', reflect(fragment))
            return response
    # If no match found in the rules, return a default response
    return "I'm sorry, I didn't quite understand that. Could you rephrase or explain further?"

# This function starts the conversation with the user.
# It keeps taking the user's input and responding until the user indicates they want to stop. 
# for Streamlit app
def talk_to_me(statement):
    if statement.lower() in ['i quit', 'i am done', 'good bye']:
        return f'Goodbye. It was nice talking to you.'

    return analyze(statement)

