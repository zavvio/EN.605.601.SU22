import random


class Wheel:
    """
    A class used to represent the Wheel of Jeopardy!
    Attributes
    -----------
    sectors : list<str>
        List of strings that represent each possible result from the wheel

    Methods
    -------
    spin()
        Spin the wheel to get a string result

    add_categories(categories_to_add)
        Adds the given categories to the wheel sectors
    """
    def __init__(self, categories):
        # self.sectors = ["Free Spin", "Lose Turn", "Bankrupt", "Player's Choice", "Opponents' Choice", "Spin Again"]
        # TODO Only using given categories for demo, remove when finished
        # self.sectors = []
        # self.add_categories(categories)
        pass

    def spin(self):
        """
        Simulates a spin of the wheel using a random number generator
        :return: str
            The name of the sector that was landed upon
        """
        # print(f'{self.sectors}')
        # print(f'len = {len(self.sectors)}')
        # return self.sectors[random.randrange(len(self.sectors))]

        return random.randint(0, 17)
        # return random.choice(self.sectors)

    def add_categories(self, categories_to_add):
        """
        Adds two of each question category to the list of sectors to spin
        :param categories_to_add: list<str>
            The list of categories that will be added
        """
        for cat in categories_to_add:
            self.sectors.extend([cat] * 2)
