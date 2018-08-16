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



    id2line={ line.split(' +++$+++ ')[0] : clean_text(line.split(' +++$+++ ')[4]) for
             line in lines if len(line.split(' +++$+++ ')) == 5}


    # Creating a list of all of the conversations
    conversations_ids = []
    for conversation in conversations[:-1]:
        _conversation = conversation.split(' +++$+++ ')[-1][1:-1].replace("'", "").replace(" ", "")
        conversations_ids.append(_conversation.split(','))


    # Getting separately the questions and the answers
    clean_questions = []
    clean_answers = []
    for conversation in conversations_ids:
        for i in range(len(conversation) - 1):
            clean_questions.append(id2line[conversation[i]])
            clean_answers.append(id2line[conversation[i+1]])

    tokens=[word for text in id2line.values() for word in text.split()]
    word2count=Counter(tokens)

    # Creating two dictionaries that map the questions words and the answers words to a unique integer
    threshold_questions = 20
    questionswords2int = {}
    word_number = 0
    for word, count in word2count.items():
        if count >= threshold_questions:
            questionswords2int[word] = word_number
            word_number += 1
    threshold_answers = 20
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

    answersints2word = {w_i: w for w, w_i in answerswords2int.items()}
    questionints2word = {w_i: w for w, w_i in questionswords2int.items()}


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
        if len(ints)<26 and len(ints)>=1:
            questions_into_int.append(ints)
    answers_into_int = []
    for answer in clean_answers:
        ints = []
        for word in answer.split():
            if word not in answerswords2int:
                ints.append(answerswords2int['<OUT>'])
            else:
                ints.append(answerswords2int[word])
        if len(ints)<26 and len(ints)>=1:
            answers_into_int.append(ints)


    questions_into_int.sort(key=len)
    answers_into_int.sort(key=len)
    return (questionswords2int, answerswords2int,questions_into_int,answers_into_int)











