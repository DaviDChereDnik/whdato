LOGGING_FORMAT = "[%(asctime)s] {%(funcName)s}  <%(levelname)s>  ||  %(message)s"
LOG_PATH = "./log.txt"

GROUP_ID = your group id
ACCESS_TOKEN = \
    "your token"
POST_MESSAGE = "● (◦'ںˉ◦) что будет завтра (◦'ںˉ◦) ●"

# If you add /zavtra in the end of CITE, will be parsed data for tomorrow
CITE = "http://kakoysegodnyaprazdnik.ru/zavtra"
DOT = "• "
BULLET = "•"  # Open Sans support only black bullet
DATE_FORMAT = "%d.%m.%Y"
# User-agent for GET to make request
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


# Path of the template svg file
TEMPLATE_PATH = "./template.svg"
# Path of the ready picture
OUTPUT_PATH = "./post.png"
# Svg namespace
SVGNS = "http://www.w3.org/2000/svg"
# Path of the font which need for know length of a string in px
FONT = "./.fonts/OpenSans.ttf"
FONT_SIZE = 14
# Min width of the max length of a text
MIN_WIDTH = 60
# Height of the row which need to calc the height of the block
ROW_HEIGHT = 15
# Max height of the block
MAX_HEIGHT = 830
# Width of the svg template which need to calc max width
SVG_WIDTH = 700
# Params which need to calc max width
DIST_FROM_EDGE_TO_TEXT = 20
DIST_FROM_DELIMITER_TO_TEXT = 20
DELIMITER_WIDTH = 7
# Params which need to add data into picture
CEL_X = '20'
HIST_X = '680'
CEL_CLASS = "celebrations_text"
HIST_CLASS = "events_text"
