from getImage import getImage

fetched = open('instance/food.sql', 'w')

with open('instance/initialFood.sql', 'r') as food:
    for line in food.readlines():
        if "CREATE TABLE recipes" in line:
            fetched.write(f"{line[:-3]}, imageURL VARCHAR NOT NULL);\n")
        elif "INSERT INTO recipes" in line:
            title = line.split("'")[1]
            url = getImage(title)
            fetched.write(f"{line[:-3]}, '{url}');\n")
        else:
            fetched.write(line)

fetched.close()
