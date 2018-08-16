import os
from os import path

here = path.abspath(path.dirname(__file__))


class chatBotConfig:
    input_file_name=[here+'/../data/movie_lines.txt',here+'/../data/movie_conversations.txt']
    threshold_questions = 20
    threshold_answers = 20
