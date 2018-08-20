from os import path

here = path.abspath(path.dirname(__file__))


class chatBotConfig:
    input_file_name=[here+'/../data/movie_lines.txt',here+'/../data/movie_conversations.txt']
    threshold_questions = 20
    threshold_answers = 20
    
    # Setting the Hyperparameters
    epochs = 100
    batch_size = 32
    rnn_size = 1024
    num_layers = 3
    encoding_embedding_size = 1024
    decoding_embedding_size = 1024
    learning_rate = 0.001
    learning_rate_decay = 0.9
    min_learning_rate = 0.0001
    keep_probability = 0.5
