class SummAllNum:
    @staticmethod
    def sum_of_list(numbers):
        if not all(isinstance(n, (int, float)) for n in numbers):
            raise ValueError("Все элементы списка должны быть числами")
        return sum(numbers)