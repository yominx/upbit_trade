import logging

mylogger = logging.getLogger("TRADE")


def logInit():
    mylogger = logging.getLogger("TRADE")
    mylogger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    stream_hander = logging.StreamHandler()
    stream_hander.setFormatter(formatter)
    mylogger.addHandler(stream_hander)

    file_handler = logging.FileHandler('trade.log')
    file_handler.setFormatter(formatter)
    mylogger.addHandler(file_handler)


def logPrint(message):
    mylogger.info(message)

