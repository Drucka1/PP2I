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

def knapsack(maxBudget: int, recipes: list, prices: list) -> int:
    memo = {}
    def currentPrice(recipes: list, prices: list):
        return sum([prices[i] if recipe else 0 for i, recipe in enumerate(recipes)])

    def addRecipe(currentRecipes: list, index: int):
        return [1 if i == index else recipe for i, recipe in enumerate(currentRecipes)]

    def solve(depth: int, maxBudget:int, recipes: list, prices: list) -> list:
        if depth < 0:
            return recipes

        if (depth, maxBudget) in memo:
            return memo[(depth, maxBudget)]

        takeBudget = maxBudget - prices[depth]
        noTake = solve(depth - 1, maxBudget, recipes, prices) 
        noTakePrice = currentPrice(noTake, prices)
        if 0 <= takeBudget:
            takeRecipes = addRecipe(recipes, depth)
            take = solve(depth - 1, takeBudget, takeRecipes, prices)
            takePrice = currentPrice(take, prices)

            if noTakePrice <= takePrice:
                result = take
            else:
                result = noTake
        else:
            result = noTake

        memo[(depth, maxBudget)] = result
        return result

    maxDepth = len(recipes) - 1
    budget = maxBudget - currentPrice(recipes, prices)
    return solve(maxDepth, budget, recipes, prices)
        


if __name__ == "__main__":
    print(knapsack(13, [0, 0, 0, 0, 0], [3, 3, 3, 3, 3])) 
    
