"""Represents executable entrypoint for `weather` application."""
from weather.address import Address
from main import easyrun


if __name__ == '__main__':
    easyrun(address=Address())
