# python-postnl-api

Python wrapper for the PostNL API (Dutch Postal Services), which can be used to track packages and letter deliveries.

```python
from postnl_api import PostNL_API

postnl = PostNL_API('email@domain.com', 'password')

# Get relevant shipments
shipments = postnl.get_relevant_shipments()

for shipment in shipments:
    print (shipment['key'])

# Get letters
letters = postnl.get_letters()
print (letters)
```