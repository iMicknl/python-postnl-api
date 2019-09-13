import argparse
from postnl_api import PostNL_API


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Run the test for PostNL_API")
    parser.add_argument("username", type=str, help="Your username (email address)")
    parser.add_argument("password", type=str, help="Your password")
    args = parser.parse_args()
    username = args.username
    password = args.password
    # Login using your jouw.postnl.nl credentials
    api = PostNL_API(username, password, 5)

    # Get packages
    print("Get packages")
    packages = api.get_deliveries()
    print("Number of packages to be delivered: ", len(packages))
    print("Listing packages:")
    [print(p) for p in packages]

    packages = api.get_distributions()
    print("Number of packages to be distributed: ", len(packages))
    print("Listing packages:")
    [print(p) for p in packages]

    if api.is_letters_activated:
        letters = api.get_letters()
        print("Number of letters: ", len(letters))
        print("Listing letters:")
        [print(l) for l in letters]


if __name__ == "__main__":
    main()
