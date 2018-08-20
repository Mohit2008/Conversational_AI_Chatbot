from collections import Counter
import os
import sys
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir, os.pardir))
from Chatbot.config import chatBotConfig
from TextCleaning import clean_text


def pre_process():
    # Importing the dataset
    lines = open(chatBotConfig.input_file_name[0], encoding = 'utf-8',
                 errors = 'ignore').read().split('\n')
    conversations = open(chatBotConfig.input_file_name[1], encoding = 'utf-8',
                         errors = 'ignore').read().split('\n')
    
     
    # Creating a dictionary that maps each line and its id
    id2line = {}
    for line in lines:
        _line = line.split(' +++$+++ ')
        if len(_line) == 5:
            id2line[_line[0]] = _line[4]
     
    # Creating a list of all of the conversations
    conversations_ids = []
    for conversation in conversations[:-1]:
        _conversation = conversation.split(' +++$+++ ')[-1][1:-1].replace("'", "").replace(" ", "")
        conversations_ids.append(_conversation.split(','))
     
    # Getting separately the questions and the answers
    questions = []
    answers = []
    for conversation in conversations_ids:
        for i in range(len(conversation) - 1):
            questions.append(id2line[conversation[i]])
            answers.append(id2line[conversation[i+1]])
     
    # Cleaning the questions
    clean_questions = []
    for question in questions:
        clean_questions.append(clean_text(question))
     
    # Cleaning the answers
    clean_answers = []
    for answer in answers:
        clean_answers.append(clean_text(answer))
     
    # Filtering out the questions and answers that are too short or too long
    short_questions = []
    short_answers = []
    i = 0
    for question in clean_questions:
        if 2 <= len(question.split()) <= 25:
            short_questions.append(question)
            short_answers.append(clean_answers[i])
        i += 1
    clean_questions = []
    clean_answers = []
    i = 0
    for answer in short_answers:
        if 2 <= len(answer.split()) <= 25:
            clean_answers.append(answer)
            clean_questions.append(short_questions[i])
        i += 1
     
    # Creating a dictionary that maps each word to its number of occurrences
    word2count = {}
    for question in clean_questions:
        for word in question.split():
            if word not in word2count:
                word2count[word] = 1
            else:
                word2count[word] += 1
    for answer in clean_answers:
        for word in answer.split():
            if word not in word2count:
                word2count[word] = 1
            else:
                word2count[word] += 1
     
    # Creating two dictionaries that map the questions words and the answers words to a unique integer
    threshold_questions = 15
    questionswords2int = {}
    word_number = 0
    for word, count in word2count.items():
        if count >= threshold_questions:
            questionswords2int[word] = word_number
            word_number += 1
    threshold_answers = 15
    answerswords2int = {}
    word_number = 0
    for word, count in word2count.items():
        if count >= threshold_answers:
            answerswords2int[word] = word_number
            word_number += 1
     
    # Adding the last tokens to these two dictionaries
    tokens = ['<PAD>', '<EOS>', '<OUT>', '<SOS>']
    for token in tokens:
        questionswords2int[token] = len(questionswords2int) + 1
    for token in tokens:
        answerswords2int[token] = len(answerswords2int) + 1
     
    # Creating the inverse dictionary of the answerswords2int dictionary
    answersints2word = {w_i: w for w, w_i in answerswords2int.items()}
     
    # Adding the End Of String token to the end of every answer
    for i in range(len(clean_answers)):
        clean_answers[i] += ' <EOS>'
     
    # Translating all the questions and the answers into integers
    # and Replacing all the words that were filtered out by <OUT> 
    questions_into_int = []
    for question in clean_questions:
        ints = []
        for word in question.split():
            if word not in questionswords2int:
                ints.append(questionswords2int['<OUT>'])
            else:
                ints.append(questionswords2int[word])
        questions_into_int.append(ints)
    answers_into_int = []
    for answer in clean_answers:
        ints = []
        for word in answer.split():
            if word not in answerswords2int:
                ints.append(answerswords2int['<OUT>'])
            else:
                ints.append(answerswords2int[word])
        answers_into_int.append(ints)
     
    # Sorting questions and answers by the length of questions
    sorted_clean_questions = []
    sorted_clean_answers = []
    for length in range(1, 25 + 1):
        for i in enumerate(questions_into_int):
            if len(i[1]) == length:
                sorted_clean_questions.append(questions_into_int[i[0]])
                sorted_clean_answers.append(answers_into_int[i[0]])
    
    return (questionswords2int, answerswords2int,sorted_clean_questions,sorted_clean_answers,answersints2word)
 