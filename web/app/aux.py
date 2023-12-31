def deleteOccurences(l: list) -> list:
    return list(dict.fromkeys(l))

def deleteOccurencesIngredients(l: list) -> list:
    seen = set()
    result = []
    for d in l:
        # Convert the dictionary to a frozenset to make it hashable
        frozenset_d = frozenset(d.items())
        if frozenset_d not in seen:
            seen.add(frozenset_d)
            result.append(d)
    return result

def search(query: str, data: list) -> list:
    found = []
    for item in data:
        if query.lower() in item[0].lower():
            found.append(item)
    return found

if __name__ == "__main__":
    print(deleteOccurences([1,1,2,3,4]))
