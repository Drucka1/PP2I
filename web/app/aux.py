def deleteOccurences(l: list) -> list:
    return list(dict.fromkeys(l))

def search(query: str, data: list) -> list:
    found = []
    for item in data:
        if query.lower() in item[0].lower():
            found.append(item)
    return found

if __name__ == "__main__":
    print(deleteOccurences([1,1,2,3,4]))
