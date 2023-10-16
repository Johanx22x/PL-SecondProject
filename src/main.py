from food import Food, FoodType


class Program:
    def run(self):
        """Main entry point of the program."""
        ...


if __name__ == "__main__":
    rice = (Food()
            .with_id(0)
            .with_type(FoodType.PROTEIN)
            .with_name("Rice")
            .with_calories(70))
    print(rice)
    Program().run()
