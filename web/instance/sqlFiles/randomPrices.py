from random import random

def randomPrices(file: str, maxPrice: float) -> None:
    newFile = open('randomPrices.sql', 'w')
    with open(file, 'r') as f:
        for line in f:
            if "CREATE TABLE IF NOT EXISTS ingredients(" in line:
                newFile.write(line[:-3] + ", price REAL NOT NULL);\n")
            elif "INSERT INTO ingredients VALUES" in line:
                price = maxPrice * random()
                newFile.write(line[:-3] + ", {:.2f});\n".format(price))
            else:
                newFile.write(line)
            

if __name__ == "__main__":
    randomPrices('food.sql', 5)

