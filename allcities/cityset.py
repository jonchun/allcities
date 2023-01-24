#!/usr/bin/env python3
# coding: utf-8

import logging
import operator
import random
import re

from allcities.city import City

logger = logging.getLogger('allcities.geonamesdata')


class CitySet(set):
    """
    Wrapper that represents a set of cities.
    """
    wrapped_methods = ('difference',
                       'intersection',
                       'symmetric_difference',
                       'union',
                       'copy'
                      )

    wrapped_bool_methods = ('issubset', 'isdisjoint')

    def __new__(cls, iterable):
        selfobj = super().__new__(CitySet)
        selfobj._set = set(iterable)

        for method_name in cls.wrapped_methods:
            setattr(selfobj, method_name, cls._wrap_method(method_name, selfobj))

        for method_name in cls.wrapped_bool_methods:
            setattr(selfobj, method_name, cls._wrap_bool_method(method_name, selfobj))

        return selfobj

    @classmethod
    def _wrap_method(cls, method_name, obj):
        def method(*args, **kwargs):
            result = getattr(obj._set, method_name)(*args, **kwargs)
            return CitySet(result)
        return method

    @classmethod
    def _wrap_bool_method(cls, method_name, obj):
        def method(*args, **kwargs):
            result = getattr(obj._set, method_name)(*args, **kwargs)
            return result
        return method

    def __init__(self, iterable):
        pass

    def __len__(self):
        return len(self._set)

    def __iter__(self):
        return iter(self._set)

    def __contains__(self, item):
        return item in self._set

    def __repr__(self):
        return '<CitySet ({})>'.format(len(self))

    @property
    def random(self):
        return random.choice(self._set)
    
    def filter(self, **kwargs):
        """
        Case insensitive search for all cities that contain a keyword based on field.
        This method only supports searching of fields that have string based values and
        includes the strings contained within the 'alternatenames' list.
        """
        city = City()
        subset_cities = self._set
        str_fields = [field
                      for field in city.ordered_fields
                      if isinstance(getattr(city, field), (str, list))
                     ]
        num_fields = [field
                      for field in city.ordered_fields
                      if isinstance(getattr(city, field), (int, float))
                     ]

        for kwarg, value in kwargs.items():
            if kwarg in str_fields:
                subset_cities = [city
                                 for city in subset_cities
                                 if CitySet.attribute_contains(city, kwarg, value)
                                ]
            elif kwarg in num_fields:
                subset_cities = [city
                                 for city in subset_cities
                                 if CitySet.attribute_compare(city, kwarg, value)
                                ]
            else:
                raise InvalidFilterException('{} is not a valid property!'.format(kwarg))


        return CitySet(subset_cities)

    @staticmethod
    def attribute_compare(city, attribute_name, check_value):
        """
        Check if attribute contains value. Numeric comparisons.
        """
        pattern = r'([!><=]{1,2})\s*([\.\d]+)'
        match = re.match(pattern, check_value.strip())

        if not match:
            raise InvalidFilterException('Numeric comparisons must be in the form "[operator] [value]". E.g. "> 5"')

        lookup_table = {
            '<': operator.lt,
            '<=': operator.le,
            '==': operator.eq,
            '=': operator.eq,
            '!=': operator.ne,
            '>': operator.gt,
            '>=': operator.ge
        }
        try:
            compare_fnc = lookup_table[match.group(1)]
        except KeyError:
            raise InvalidFilterException('Invaliid Operator!')

        # cast the check value to a float
        compare_val = float(match.group(2))
        attribute_value = getattr(city, attribute_name, None)
        if not attribute_value:
            return False
        return compare_fnc(attribute_value, compare_val)

    @staticmethod
    def attribute_contains(city, attribute_name, check_value):
        """
        Check if attribute contains value. (string comparison only with
        special exception for alternatenames)
        """
        check_value = check_value.lower()
        attribute_value = getattr(city, attribute_name, None)

        # Special handling for alternate names
        if isinstance(attribute_value, list):
            for attr_val in attribute_value:
                if check_value in attr_val.lower():
                    return True
            return False

        # Return if string is a match to attribute value
        return check_value in attribute_value.lower()

class InvalidFilterException(Exception):
    pass
