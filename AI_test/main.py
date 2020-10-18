import sys
import queue
import threading
import json
import collections
import time
import logging

logging.basicConfig(level=logging.DEBUG, filename='/Users/tmssmith/StS_AI/AI_test/log.log')

def read_stdin(input_queue):
    """Read lines from stdin and write them to a queue

    :param input_queue: A queue, to which lines from stdin will be written
    :type input_queue: queue.Queue
    :return: None
    """
    while True:
        stdin_input = ""
        while True:
            input_char = sys.stdin.read(1)
            if input_char == '\n':
                break
            else:
                stdin_input += input_char
        input_queue.put(stdin_input)


def write_stdout(output_queue):
    """Read lines from a queue and write them to stdout

    :param output_queue: A queue, from which this function will receive lines of text
    :type output_queue: queue.Queue
    :return: None
    """
    while True:
        output = output_queue.get()
        logging.debug('Write: {}'.format(output))
        print(output, end='\n', flush=True)


class Coordinator:
    """An object to coordinate communication with Slay the Spire"""

    def __init__(self):
        self.input_queue = queue.Queue()
        self.output_queue = queue.Queue()
        self.input_thread = threading.Thread(target=read_stdin, args=(self.input_queue,))
        self.output_thread = threading.Thread(target=write_stdout, args=(self.output_queue,))
        self.input_thread.daemon = True
        self.input_thread.start()
        self.output_thread.daemon = True
        self.output_thread.start()
        self.action_queue = collections.deque()
        self.state_change_callback = None
        self.out_of_game_callback = None
        self.error_callback = None
        self.game_is_ready = False
        self.stop_after_run = False
        self.in_game = False
        self.last_game_state = None
        self.last_error = None

    def signal_ready(self):
        """Indicate to Communication Mod that setup is complete

        Must be used once, before any other commands can be sent.
        :return: None
        """
        # print('signal ready')
        self.send_message("ready")

    def send_message(self, message):
        """Send a command to Communication Mod and start waiting for a response

        :param message: the message to send
        :type message: str
        :return: None
        """
        self.output_queue.put(message)
        self.game_is_ready = False

    def get_next_raw_message(self, block=False):
        """Get the next message from Communication Mod as a string

        :param block: set to True to wait for the next message
        :type block: bool
        :return: the message from Communication Mod
        :rtype: str
        """
        if block or not self.input_queue.empty():
            return self.input_queue.get()


coordinator = Coordinator()
coordinator.signal_ready()

while True:
    message = coordinator.get_next_raw_message(False)
    if message is not None:
        logging.debug('Read: {}'.format(message))
