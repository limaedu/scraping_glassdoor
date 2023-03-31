import logging

class MyLog:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        self.file_handler = logging.FileHandler(f'{name}_log.log')
        self.file_handler.setLevel(logging.DEBUG)
        self.file_handler.setFormatter(logging.Formatter('%(asctime)s-%(levelname)s-%(message)s'))
        
        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setLevel(logging.DEBUG)
        self.stream_handler.setFormatter(logging.Formatter('%(asctime)s-%(levelname)s-%(message)s'))
        
        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.stream_handler)

        


