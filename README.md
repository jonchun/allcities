# allcities
> a Python library to work with all the cities of the world with a population of at least 1000 inhabitants.

## Note
This library was whipped up in an afternoon when I got a little carried away when I really needed something much simpler. It is not fully tested and will need revisiting/cleanup.

## Installation
```sh
pip install allcities
```

## Usage example
Usage of this library is quite simple.
```python
from allcities import cities

results = cities.filter(name='Los Angeles')
for result in results:
    print(result)
```
`cities` is a set-like object that contains objects that represent cities. The above code will output:
```
<Santa Rosa los Angeles, 11, MX>
<Los Angeles, 10, MX>
<Los Angeles, CA, US>
<Los Angeles, 25, MX>
<Lake Los Angeles, CA, US>
<East Los Angeles, CA, US>
<Los Angeles, 13, PH>
```
You can chain/combine filters as follows:
```python
results = cities.filter(name='Los Angeles').filter(country_code='US')
results2 = cities.filter(name='Los Angeles', country_code='US')
print(results == results2)
for result in results:
    print(result)
```
gives you
```
True
<Los Angeles, CA, US>
<East Los Angeles, CA, US>
<Lake Los Angeles, CA, US>
```

You can also filter on numeric properties. The syntax to do so is a comparison operator `<, <=, ==, !=, >=, >` followed by a numeric value.
```python
results = cities.filter(elevation='>1000')
results2 = cities.filter(elevation='>1000').filter(elevation='<1500')
print(results)
print(results2)
```
Gives you
```
<CitySet (1339)>
<CitySet (795)>
```
Each city object has properties that can be accessed normally or filtered on. You can also export a dictionary with the `.dict` property.
```python
pprint.pprint(city_object.dict)
```
Here is the resulting dict
```python
{'admin1_code': 'CA',
 'admin2_code': '037',
 'alternatenames': ['East Los Angeles',
                    'Este de Los Angeles',
                    'Este de Los Ángeles',
                    'Ist Los Andzeles',
                    'Orienta Losangeleso',
                    'Orienta Losanĝeleso',
                    'dong luo shan ji',
                    'iseuteuloseuaenjelleseu',
                    'ista lasa enjelsa',
                    'isutorosanzerusu',
                    'Ист Лос Анџелес',
                    'इस्ट लस एन्जेल्स',
                    'イーストロサンゼルス',
                    '东洛杉矶',
                    '이스트로스앤젤레스'],
 'asciiname': 'East Los Angeles',
 'country_code': 'US',
 'dem': 63,
 'elevation': 61,
 'feature_class': 'P',
 'feature_code': 'PPL',
 'geonameid': 5344994,
 'latitude': 34.0239,
 'longitude': -118.17202,
 'modification_date': '2011-05-14',
 'name': 'East Los Angeles',
 'population': 126496,
 'timezone': 'America/Los_Angeles'}
 ```

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Release History
* 1.0.0
    * Initial Release

## Contributing
1. Fork it (<https://github.com/Jonchun/allcities/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
