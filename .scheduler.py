from coreAnalyzer import *
from notifications import *

if __name__ == "__main__":
    result = marketSummarize()
    telegram_sendMessage(result)