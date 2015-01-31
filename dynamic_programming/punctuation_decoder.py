# -*- coding: utf-8 -*-

"""
You are given a string of characters, which you believe to be a corrupted text document
in which all punctuation has vanished (so that it looks something like “itwasthebestoftimes...”).
You wish to reconstruct the document using a dictionary.
"""

from graph_shortest_path import memoize


class DecodedText(object):
    """
    Decoded text
    """

    def __init__(self, successful=True):
        self.decoded_string = []
        self.successful = successful

    def add(self, word):
        self.decoded_string.append(word)

    def __nonzero__(self):
        return self.successful

    def copy(self):
        c = DecodedText(self.successful)
        c.decoded_string = self.decoded_string[:]
        return c

    def __str__(self):
        return ' '.join(self.decoded_string)


class Decoder(object):
    """
    Use dynamic programming approach to decode the string.
    Running time is O(N^2)
    """

    def __init__(self, words):
        self.words = words

    @memoize
    def decode(self, string, length=None):
        """
        Returns True if the string is decodable for a given position
        """
        if length is None:
            length = len(string)
        elif length == 0:
            # an empty string is decodable by default
            return DecodedText(True)

        for i in xrange(length):
            # if the substring is in dict and the remaining substring is decodable
            remained_decoded = self.decode(string, i)
            if string[i:length] in self.words and remained_decoded:
                decoded = remained_decoded.copy()
                decoded.add(string[i:length])
                return decoded
        return DecodedText(False)


if __name__ == '__main__':
    words = set(['i', 'it', 'was', 'the', 'he', 'be', 'best', 'of', 'time', 'times'])
    decoder = Decoder(words)
    result = decoder.decode('itwasthebestoftimes')
    assert str(result) == 'it was the best of times'
