from PIL import ImageFont
import logging
from cairosvg import svg2png
from lxml import etree
from const import *


class Picture:
    def __init__(self, celebrations, historical_events, date):
        # Check that all args have need type
        if type(celebrations) is not list:
            logging.error("Attr 'celebrations' has unacceptable type")
            return
        if type(historical_events) is not list:
            logging.error("Attr 'historical_events' has unacceptable type")
            return
        if type(date) is not str:
            logging.error("Attr 'date' has unacceptable type")
            return

        self.celebrations = celebrations
        self.historical_events = historical_events
        self.date = date

        self.max_length = 0
        self.data_struct = \
            {'cel':  [],
             'hist': []}

        self.font = ImageFont.truetype(FONT, FONT_SIZE)

        logging.info("Starting reading svg template file")
        try:
            svg_file = open(TEMPLATE_PATH)
        except OSError:
            logging.error("Open svg template file have been failed")
            return
        else:
            logging.info("Svg template file have been opened")
        self.svgCode = svg_file.read()
        svg_file.close()
        # Encoding this svg code to utf-8, because lxml.etree works with utf-8
        self.svgCode = self.svgCode.encode('utf-8')
        logging.info("Successfully write svg code to var")

        # Parse svg code from a var
        self.xml_data = etree.fromstring(self.svgCode)

    def __add_date(self):
        # Find a need tspan (or other elem) with id "date", where s (SVGNS) - xml namespace
        # In success find_text(xml) will return [<ELement {SVGNS}need element in ...>]
        find_text = etree.ETXPath("//{%s}tspan[@id='date']" % SVGNS)
        if not find_text(self.xml_data):
            logging.error("Incorrect or nonexistent attr")
            return
        else:
            logging.info("Successfully find date element")

        # Replace a template date
        find_text(self.xml_data)[0].text = self.date
        new_svg = etree.tostring(self.xml_data)
        # Write a result to a self var of svg code
        self.svgCode = new_svg
        logging.info("Successfully change the date")

    def __calc_length(self):
        # Hf - half
        hf_width = SVG_WIDTH / 2
        hf_delimiter = DELIMITER_WIDTH / 2
        self.max_length = \
            hf_width - (DIST_FROM_EDGE_TO_TEXT + DIST_FROM_DELIMITER_TO_TEXT + hf_delimiter)
        round(self.max_length)  # Rounds to the nearest even
        if self.max_length < MIN_WIDTH:
            logging.error("Max length too small")
        else:
            logging.info("Successfully calculated max length")

    def __split_list(self, source):
        if type(source) is not list:
            logging.error("Attr 'source' has an unacceptable type")
            return

        result = []

        logging.info("Start to splitting list")
        for index in range(len(source)):
            if self.font.getsize(source[index])[0] <= self.max_length:
                result.append([source[index]])
                continue
            else:
                # Cut and add the first elem of result
                inter_result = source[index]
                cut_off = ""
                inner_cut_off = ""
                # Get and append the first element of list
                while self.font.getsize(inter_result)[0] > self.max_length:
                    # Put the last word into cut_off
                    cut_off = inter_result.split()[-1] + ' ' + cut_off
                    # Delete the last word from inter_result
                    inter_result = inter_result.rsplit(' ', 1)[0]
                else:
                    result.append([inter_result])

                # Cut and append the rest
                while cut_off != "":
                    if self.font.getsize(cut_off)[0] <= self.max_length:
                        result[index].append(cut_off)
                        # We do it to continue cut the remaining text off
                        cut_off = inner_cut_off
                        inner_cut_off = ""
                    else:
                        inner_cut_off = cut_off.split()[-1] + ' ' + inner_cut_off
                        cut_off = cut_off.rsplit(maxsplit=1)[0]

        logging.info("Successfully split the list")
        return result

    def __prepare_struct(self):
        # We need delete an empty lists
        self.data_struct['cel'] = \
            [x for x in self.__split_list(self.celebrations) if x != ['']]
        self.data_struct['hist'] = \
            [x for x in self.__split_list(self.historical_events) if x != ['']]

    def __add_bullets(self):
        # Because cel block has a start anchor, but hist block has an end anchor
        # Way to add bullet to this blocks are different

        for event in range(len(self.data_struct['cel'])):
            self.data_struct['cel'][event][0] = \
                BULLET + ' ' + self.data_struct['cel'][event][0]

        for event in range(len(self.data_struct['hist'])):
            self.data_struct['hist'][event][0] += ' ' + BULLET

    def __add_info(self, key):
        if key != 'cel' and key != 'hist':
            logging.error('Key {} is incorrect'.format(key))
            return

        # Find need parent
        # ns - namespace, within it found a parent will unreachable
        parent_class = self.xml_data.find(".//ns:text[@class='{}']".format(
                                        CEL_CLASS if key == 'cel' else HIST_CLASS),
                                           {'ns': SVGNS})
        if parent_class is None:
            logging.error('Incorrect name of class')
            return

        dy = 0
        height = 0
        # Adding need data to picture
        for event in range(len(self.data_struct[key])):
            # If all data exceeds the allowable height in px, we stop add new data to picture
            if height > MAX_HEIGHT:
                break
            for line in range(len(self.data_struct[key][event])):
                parent_class.append(etree.XML(
                    "<tspan {attr}>{text}</tspan>".format(
                        text=self.data_struct[key][event][line],
                        attr="x='{x}' dy='{dy}'".format(
                            x=CEL_X if key == 'cel' else HIST_X,
                            dy=str(dy) + 'em',
                        )
                    )
                ))
                height += ROW_HEIGHT

                if len(self.data_struct[key][event]) > 1:
                    dy = 1.1

            height += ROW_HEIGHT
            dy = 2

        new_svg = etree.tostring(self.xml_data)
        self.svgCode = new_svg
        logging.info('Successfully add {} data to picture'.format(key))

    def __prepare_picture(self):
        self.__add_date()

        self.__calc_length()
        self.__prepare_struct()
        self.__add_bullets()
        self.__add_info('cel')
        self.__add_info('hist')
        logging.info("Got a ready svg-picture")

    def __convert_picture(self):
        self.__prepare_picture()
        svg2png(bytestring=self.svgCode, write_to=OUTPUT_PATH)
        logging.info("SVG picture have been converted into PNG picture")

    def get_picture(self):
        self.__convert_picture()
