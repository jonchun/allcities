#!/usr/bin/env python3
# coding: utf-8

import logging

logger = logging.getLogger('allcities.geonamesdata')

class City:
    ordered_fields = ['geonameid', 'name', 'asciiname', 'alternatenames', 'latitude', 'longitude',
                      'feature_class', 'feature_code', 'country_code', 'cc2', 'admin1_code',
                      'admin2_code', 'admin3_code', 'admin4_code', 'population', 'elevation', 'dem',
                      'timezone', 'modification_date']
    def __init__(self):
        self.geonameid = 0
        self.name = ''
        self.asciiname = ''
        self.alternatenames = []
        self.latitude = 0.0
        self.longitude = 0.0
        self.feature_class = ''
        self.feature_code = ''
        self.country_code = ''
        self.cc2 = ''
        self.admin1_code = ''
        self.admin2_code = ''
        self.admin3_code = ''
        self.admin4_code = ''
        self.population = 0
        self.elevation = 0
        self.dem = 0
        self.timezone = ''
        self.modification_date = ''

    def __repr__(self):
        return '<{}, {}, {}>'.format(self.name, self.admin1_code, self.country_code)

    @property
    def dict(self):
        city_dict = {}
        for field_name in self.ordered_fields:
            field_value = getattr(self, field_name)
            if field_value:
                city_dict[field_name] = field_value
        return city_dict

    @classmethod
    def geonames_factory(cls, geonames_list):
        """
        Takes a list of parameters from a geonames.org dump.

        The main 'geoname' table has the following fields :
        ---------------------------------------------------
        0 geonameid         : integer id of record in geonames database
        1 name              : name of geographical point (utf8) varchar(200)
        2 asciiname         : name of geographical point in plain ascii characters, varchar(200)
        3 alternatenames    : alternatenames, comma separated, ascii names automatically transliterated, convenience attribute from alternatename table, varchar(10000)
        4 latitude          : latitude in decimal degrees (wgs84)
        5 longitude         : longitude in decimal degrees (wgs84)
        6 feature class     : see http://www.geonames.org/export/codes.html, char(1)
        7 feature code      : see http://www.geonames.org/export/codes.html, varchar(10)
        8 country code      : ISO-3166 2-letter country code, 2 characters
        9 cc2               : alternate country codes, comma separated, ISO-3166 2-letter country code, 200 characters
        10 admin1 code       : fipscode (subject to change to iso code), see exceptions below, see file admin1Codes.txt for display names of this code; varchar(20)
        11 admin2 code       : code for the second administrative division, a county in the US, see file admin2Codes.txt; varchar(80) 
        12 admin3 code       : code for third level administrative division, varchar(20)
        13 admin4 code       : code for fourth level administrative division, varchar(20)
        14 population        : bigint (8 byte int) 
        15 elevation         : in meters, integer
        16 dem               : digital elevation model, srtm3 or gtopo30, average elevation of 3''x3'' (ca 90mx90m) or 30''x30'' (ca 900mx900m) area in meters, integer. srtm processed by cgiar/ciat.
        17 timezone          : the iana timezone id (see file timeZone.txt) varchar(40)
        18 modification date : date of last modification in yyyy-MM-dd format
        """
        city = cls()
        ordered_fields = city.ordered_fields

        for index, field_value in enumerate(geonames_list):
            # We split the alternatenames column into a list of strings.
            field_name = ordered_fields[index]
            if field_name == 'alternatenames':
                field_value = field_value.split(',')
            try:
                field_type = type(getattr(city, field_name))
                # Try to cast the field to the correct default type.
                setattr(city, field_name, field_type(field_value))
            except (TypeError, ValueError):
                """
                If we are having trouble type casting because the field was empty, we insert
                None instead.
                """
                if not field_value:
                    setattr(city, field_name, None)
                else:
                    logger.error('Types Incompatible. field:{}, value_type:{}'.format(field_name, type(field_value)))
                    setattr(city, field_name, field_value)

        return city
