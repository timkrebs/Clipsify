from flask import Flask
from utils.log_config import Logger

logger = Logger(__name__).get_logger()
app = Flask(__name__)
