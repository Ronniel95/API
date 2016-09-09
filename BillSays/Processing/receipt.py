import re
from difflib import get_close_matches
from collections import defaultdict, OrderedDict

class Receipt(object):
    def __init__(self, config, raw):
        self.config = config
        self.place = self.service = self.date = self.dish = self.sum = self.dish_list = self.formed_dish_list = None
        self.raw = [line.decode('utf-8') for line in raw]
        self.raw = [v.lower() for v in self.raw]
        self.parse()

    def parse(self):
        self.place = self.parse_place()
        self.service = self.parse_service()
        self.date = self.parse_date()
        self.sum = self.parse_sum()
        # self.dish = self.parse_dish()
        self.dish_list = self.parse_line_dish()
        self.formed_dish_list = self.form_dish_list()
        self.print_formed_dish_list()

    def fuzzy_find(self, keyword, accuracy):
        """
        Returns the first line in lines that contains a keyword.
        It runs a fuzzy match if 0 < accuracy < 1.0
        :param keyword: The keyword string to look for
        :param accuracy: Required accuracy for a match of a string with the keyword
        """
        for line in self.raw:
            words = line.split()
            # Get the single best match in line
            matches = get_close_matches(keyword, words, 1, accuracy)
            if matches:
                return line

    def parse_date(self):
        for line in self.raw:
            is_phone = False
            m = re.match(self.config.date_format, line)
            # Is this line phone number format
            # if re.search(self.config.phone_format, line):
            #     is_phone = True
            # if not is_phone and m:
            if m:
                # TODO: check phone number not match with date
                # We're happy with the first match for now
                return m.group(1)

    def parse_line_dish(self):
        dish_list = []
        for line in self.raw:
            m = re.search(self.config.dish_format, line)
            # if (line == -1) and  not is_merged:
            #     if re.search(self.config.dish_format, line + 1)

            if m:
                # Check if we reached sum point etc. we need to stop find dishes
                if self.parse_sum_keyword(line):
                    return dish_list
                else:
                    # TODO : Try to use more flexible constructions
                    # Check is line date or phone number
                    is_date = is_phone_number = is_time = False
                    if re.search(self.config.date_format, line):
                        is_date = True
                    if re.search(self.config.phone_format, line):
                        is_phone_number = True
                    if re.search(self.config.time_format, line):
                        is_time = True
                        # If line is not sum line or not data phone etc.  we guess that it is dish
                    if not is_date and not is_phone_number and not is_time:
                        dish_list.append(line)
        return dish_list

    def parse_place(self):
        for int_accuracy in range(10, 6, -1):
            accuracy = int_accuracy / 10.0
            for place, spellings in self.config.places.items():
                for spelling in spellings:
                    line = self.fuzzy_find(spelling, accuracy)
                    if line:
                        # print line, accuracy,place
                        return place

    def parse_service(self):
        for int_accuracy in range(10, 5, -1):
            accuracy = int_accuracy / 10.0
            for service, spellings in self.config.service.items():
                for spelling in spellings:
                    line = self.fuzzy_find(spelling, accuracy)
                    if line:
                        #print line  # , accuracy, service
                        #return service
                        return line

    def form_dish_list(self):
        formed_dish_list = OrderedDict()
        for item in self.dish_list:
            # TODO: make splitting in form "only name of dish" : amount , price
            name_dish = re.split(self.config.dish_format, item)[0]
            # amount = re.search(self.config.amount_format, item).group(0)
            price = re.search(self.config.dish_format, item).group(0)
            price = self.correct_mistakes(price)
            # formed_dish_list.update({name_dish: [amount, price]})
            formed_dish_list.update({name_dish: price})
        return formed_dish_list


    def print_formed_dish_list(self):
        for keys, values in self.formed_dish_list.items():
            print(keys)
            print values  # [0]
            # print values[1]

    def parse_sum(self):
        for sum_key in self.config.sum_keys:
            sum_line = self.fuzzy_find(sum_key, 0.6)
            if sum_line:
                # Replace all commas with a dot to make
                # finding and parsing the sum easier
                sum_line = sum_line.replace(',', '.')
                # Parse the sum
                sum_float = re.search(self.config.sum_format, sum_line)

                if sum_float:
                    return self.correct_mistakes(sum_float.group(0))

    def parse_sum_keyword(self, line):
        """
        Search a keyword sum in text using get_close_matches and keywords from config file
        :param line - line, which we want to check on containing keyword sum
        """

        for sum_key in self.config.dish_key_exceptions:

            words = line.split()
            # Get the single best match in line
            # TODO: Adjust parameter of accuracy empirically
            matches = get_close_matches(sum_key, words, 1, 0.7)
            if matches:
                # Replace all commas with a dot to make
                # finding and parsing the sum easier
                line = line.replace(',', '.')
                # Parse the sum
                sum_keyword = re.search(self.config.sum_format, line)
                if sum_keyword:
                    return True
        return False

    def correct_mistakes(self, line):
        cleaned_line = line
        for keys, values in self.config.rule_base.items():
            cleaned_line = cleaned_line.replace(keys, str(values))
            # keys.decode('utf-8')
            # str.lower(line)
        cleaned_line = "".join(cleaned_line.split())
        cleaned_line = cleaned_line.replace(',', '.')

        return "{0:.2f}".format(float(cleaned_line))

    # Smart dish line searchng
    # TODO: Need to rewrite with more powerful libraries and methods
    def parse_dish(self):
        for dish_key in self.config.dish_keys:
            dish_line = self.fuzzy_find(dish_key, 0.7)
            if dish_line:
                # Replace all commas with a dot to make
                # finding and parsing the sum easier
                # print dish_line
                dish_line = dish_line.replace(',', '.')
                # Parse the sum
                sum_float = re.search(self.config.dish_format, dish_line)
                if sum_float:
                    return sum_float.group(0)