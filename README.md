# python-postnl-api
(Unofficial) Python wrapper for the PostNL API (Dutch Postal Services), which can be used to track packages and letter deliveries. You can use your [jouw.postnl.nl](http://jouw.postnl.nl) credentials to use the API. 

## Quick test
```python
test_postnl_api.py USERNAME PASSWORD
```

## Code Example
```python
from postnl_api import PostNL_API

# Login using your jouw.postnl.nl credentials
postnl = PostNL_API('email@domain.com', 'password')

# Get relevant shipments
shipments = postnl.get_relevant_shipments()

for shipment in shipments:
    print (shipment['key'])

# Get letters
letters = postnl.get_letters()
print (letters)
```

## Miscellaneous
[This blogpost](https://imick.nl/reverse-engineering-the-postnl-consumer-api/) describes the process of figuring out the API endpoints and shows how this can be done for other API's.

## Changelog
See the [CHANGELOG](./CHANGELOG.md) file.

## License
MIT
