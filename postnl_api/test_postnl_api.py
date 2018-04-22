import argparse
from postnl_api import PostNL_API


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Run the test for PostNL_API")
    parser.add_argument(
        'username', type=str,
        help="Your username (email address)")
    parser.add_argument(
        'password', type=str,
        help="Your password")
    args = parser.parse_args()
    username = args.username
    password = args.password
    # Login using your jouw.postnl.nl credentials
    postnl = PostNL_API(username, password)

    # Get relevant shipments
    print("Getting shipments")
    shipments = postnl.get_relevant_shipments()
    print("Number of shipments: ", len(shipments))
    print("Listing shipments:")
    for shipment in shipments:
        print (shipment['key'])

    # Get letters
    print("Getting letters")
    letters = postnl.get_letters()
    print("Number of letters: ", len(letters))
    print("Listing letters:")
    print (letters)


if __name__ == '__main__':
    main()
