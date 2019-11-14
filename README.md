# python-postnl-api
(Unofficial) Python wrapper for the PostNL API (Dutch Postal Services), which can be used to track packages and letter deliveries. You can use your [jouw.postnl.nl](http://jouw.postnl.nl) credentials to use the API. 

## Quick test
When installed:
```python
python -m postnl_api.test_postnl_api USERNAME PASSWORD
```

Or running directly:
```python
test_postnl_api.py USERNAME PASSWORD
```

## Code Example
```python
from postnl_api import PostNL_API

# Login using your jouw.postnl.nl credentials
postnl = PostNL_API('email@domain.com', 'password')

# Get relevant deliveries
print("Getting relevant deliveries")
rel_deliveries = postnl.get_relevant_deliveries()
for delivery in rel_deliveries:
    print(delivery.debug_string)

# Get relevant deliveries
print("Getting all deliveries")
all_deliveries = postnl.get_deliveries()
for delivery in all_deliveries:
    print(delivery.debug_string)

# Get relevant deliveries
print("Getting all distributions (sent packages)")
distributions = postnl.get_distributions()
for distribution in distributions:
    print(distribution.debug_string)

# Get letters
print("Getting all letters, if that function is turned on")
letters = postnl.get_letters()
for letter in letters:
    print(letter.debug_string)
```

## Miscellaneous
[This blogpost](https://imick.nl/reverse-engineering-the-postnl-consumer-api/) describes the process of figuring out the API endpoints and shows how this can be done for other API's.

## Changelog
See the [CHANGELOG](./CHANGELOG.md) file.

## Contributors
- [@eavanvalkenburg](https://github.com/eavanvalkenburg)
- [@peternijssen](https://github.com/peternijssen)
- [@IcyPalm](https://github.com/IcyPalm)

## License
MIT
