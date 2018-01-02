from collections import defaultdict

__author__ = 'nekmo'
LISTS_TYPES = (tuple, list, set, frozenset)


class Mkv(object):
    def __init__(self):
        self.types_orders = defaultdict(lambda: 0)
        self.arguments = []

    def _normatize_input_options(self, elements):
        if not isinstance(elements, LISTS_TYPES):
            elements = list(elements)
        return ','.join(map(str, elements))

    def _auto_fill(self, type, is_default, is_forced, order):
        if order is None:
            order = self.types_orders[type]
            self.types_orders[type] += 1
        if (is_default is None and order is 0) or is_default is True:
            is_default = True
        else:
            is_default = False
        return is_default, is_forced, order

    def _order_value(self, order, value):
        if isinstance(value, bool):
            value = {True: 'yes', False: 'no'}[value]
        return '%i:%s' % (order, value)

    def _argument_value(self, argument, value):
        pattern = '-%s' if len(argument) == 1 else '--%s'
        if isinstance(value, LISTS_TYPES):
            return [pattern % argument] + list(value)
        else:
            return [pattern % argument, value]

    def set_arg(self, arg):
        self.arguments.append(arg)

    def set_arg_value(self, argument, value):
        self.arguments.extend(self._argument_value(argument, value))

    def add_language(self, language_code, name, is_default=None, is_forced=False, order=None):
        print("Default in lang", is_default)
        is_default, is_forced, order = self._auto_fill('language', is_default, is_forced, order)
        print("Default in lang", is_default)
        self.set_arg_value('language', self._order_value(order, language_code))
        self.set_arg_value('track-name', self._order_value(order,name))
        self.set_arg_value('default-track', self._order_value(order, is_default))
