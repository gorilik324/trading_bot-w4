class Arithmetic:
    @staticmethod
    def percent_increase(number: float, percentage):
        """
        Calculates the percentage increase of a number given a percentage increase.
        :param number: The original number to calculate the percentage increase from.
        :param percentage: The percentage increase as a float. For example, 10.0 for a 10% increase.
        :return: The new number after applying the percentage increase.
        """
        return number + (number * percentage) / 100


    @staticmethod
    def percent_decrease(number: float, percentage):
        """
        Calculates the percentage decrease of a number given a percentage decrease.
        :param number: The original number to calculate the percentage decrease from.
        :param percentage: The percentage decrease as a float. For example, 10.0 for a 10% decrease.
        :return: The new number after applying the percentage decrease.
        """
        return number - (number * percentage) / 100

