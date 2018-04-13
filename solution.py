from ortools.constraint_solver import pywrapcp
def main():

    # Explaining the constraints
    '''
    1. In a street there are five houses, painted five different colours.
    2. In each house lives a person of different nationality
    3. These five homeowners each drink a different kind of beverage, smoke different brand of cigar and keep a different pet.

    THE QUESTION: WHO OWNS THE FISH?

    HINTS

    1. The Brit lives in a red house.
    2. The Swede keeps dogs as pets.
    3. The Dane drinks tea.
    4. The Green house is next to, and on the left of the White house.
    5. The owner of the Green house drinks coffee.
    6. The person who smokes Pall Mall rears birds.
    7. The owner of the Yellow house smokes Dunhill.
    8. The man living in the centre house drinks milk.
    9. The Norwegian lives in the first house.
    10. The man who smokes Blends lives next to the one who keeps cats.
    11. The man who keeps horses lives next to the man who smokes Dunhill.
    12. The man who smokes Blue Master drinks beer.
    13. The German smokes Prince.
    14. The Norwegian lives next to the blue house.
    15. The man who smokes Blends has a neighbour who drinks water.
    '''

    # Create the solver
    solver = pywrapcp.Solver("einstein_riddle")

    # Create variables
    num_val = 5
    color = {
        "red" : solver.IntVar(0, num_val-1, "red"),
        "blue" : solver.IntVar(0, num_val-1, "blue"), 
        "yellow" : solver.IntVar(0, num_val-1, "yellow"), 
        "white" : solver.IntVar(0, num_val-1, "white"), 
        "green" : solver.IntVar(0, num_val-1, "green")
        }

    pet = {
        "bird" : solver.IntVar(0, num_val-1, "bird"),
        "cat" : solver.IntVar(0, num_val-1, "cat"),
        "horse" : solver.IntVar(0, num_val-1, "horse"),
        "dog" : solver.IntVar(0, num_val-1, "dog"),
        "fish" : solver.IntVar(0, num_val-1, "fish") 
        }
    
    cigar = {
        "blends" : solver.IntVar(0, num_val-1, "blends"), 
        "prince" : solver.IntVar(0, num_val-1, "prince"), 
        "pall mall" : solver.IntVar(0, num_val-1, "pall mall"), 
        "blue master" : solver.IntVar(0, num_val-1, "blue master"), 
        "dunhill" : solver.IntVar(0, num_val-1, "dunhill")
        }
    
    drink = {
        "milk" : solver.IntVar(0, num_val-1, "dunhill"), 
        "beer" : solver.IntVar(0, num_val-1, "beer"), 
        "coffee" : solver.IntVar(0, num_val-1, "coffee"), 
        "water" : solver.IntVar(0, num_val-1, "water"), 
        "tea" : solver.IntVar(0, num_val-1, "tea")
        }

    nation = {
        "brit" : solver.IntVar(0, num_val-1, "brit"),
        "swede" : solver.IntVar(0, num_val-1, "swede"),
        "dane" : solver.IntVar(0, num_val-1, "dane"), 
        "norwegian" : solver.IntVar(0, num_val-1, "norwegian"),
        "german" : solver.IntVar(0, num_val-1, "german")
        }
    
    # Add constraints
    solver.Add(solver.AllDifferent([color[key] for key in color.keys()]))
    solver.Add(solver.AllDifferent([nation[key] for key in nation.keys()]))
    solver.Add(solver.AllDifferent([cigar[key] for key in cigar.keys()]))
    solver.Add(solver.AllDifferent([pet[key] for key in pet.keys()]))
    solver.Add(solver.AllDifferent([drink[key] for key in drink.keys()]))

    '''1. The Brit lives in a red house.'''
    solver.Add(nation["brit"] == color["red"])

    '''2. The Swede keeps dogs as pets.'''
    solver.Add(nation["swede"] == pet["dog"])

    '''3. The Dane drinks tea.'''
    solver.Add(nation["dane"] == drink["tea"])

    '''4. The Green house is next to, and on the left of the White house.'''
    solver.Add(color["green"]-1 < color["white"])

    '''5. The owner of the Green house drinks coffee.'''
    solver.Add(color["green"] == drink["coffee"])

    '''6. The person who smokes Pall Mall rears birds.'''
    solver.Add(cigar["pall mall"] == pet["bird"])

    '''7. The owner of the Yellow house smokes Dunhill.'''
    solver.Add(color["yellow"] == cigar["dunhill"])

    '''8. The man living in the centre house drinks milk.'''
    solver.Add(drink["milk"] == 2)

    '''9. The Norwegian lives in the first house.'''
    solver.Add(nation["norwegian"] == 1)

    '''10. The man who smokes Blends lives next to the one who keeps cats.'''
    solver.Add(abs(cigar["blends"]-pet["cat"]) == 1)

    '''11. The man who keeps horses lives next to the man who smokes Dunhill.'''
    solver.Add(abs(pet["horse"]-cigar["dunhill"]) == 1)

    '''12. The man who smokes Blue Master drinks beer.'''
    solver.Add(cigar["blue master"] == drink["beer"])

    '''13. The German smokes Prince.'''
    solver.Add(nation["german"] == cigar["prince"])
    
    '''14. The Norwegian lives next to the blue house.'''
    solver.Add(abs(nation["norwegian"]-color["blue"]) == 1)
    
    '''15. The man who smokes Blends has a neighbour who drinks water.'''
    solver.Add(abs(cigar["blends"]-drink["water"]) == 1)

    # Decision builder
    db = solver.Phase(
                        [
                            color["red"], color["yellow"], color["blue"], color["green"], color["white"],
                            pet["dog"], pet["bird"], pet["cat"], pet["horse"], pet["fish"],
                            cigar["blends"], cigar["prince"], cigar["pall mall"], cigar["blue master"], cigar["dunhill"],
                            drink["milk"], drink["water"], drink["beer"], drink["coffee"], drink["tea"],
                            nation["norwegian"], nation["brit"], nation["swede"], nation["dane"], nation["german"]
                        ], 
                        solver.CHOOSE_FIRST_UNBOUND, 
                        solver.ASSIGN_MIN_VALUE
                    )

    # Solve
    solver.Solve(db)

    count = 0
    while solver.NextSolution():
        count += 1
        print("\n\nSolution", count, '\n')
        print("---- COLOR ----")
        print("red : ", color["red"].Value())
        print("blue : ", color["blue"].Value())
        print("yellow : ", color["yellow"].Value())
        print("green : ", color["green"].Value())
        print("white : ", color["white"].Value())

        print("---- PET ----")
        print("dog : ", pet["dog"].Value())
        print("bird : ", pet["bird"].Value())
        print("cat : ", pet["cat"].Value())
        print("horse : ", pet["horse"].Value())
        print("fish : ", pet["fish"].Value())

        print("---- CIGAR ----")
        print("blends : ", cigar["blends"].Value())
        print("prince : ", cigar["prince"].Value())
        print("pall mall : ", cigar["pall mall"].Value())
        print("blue master : ", cigar["blue master"].Value())
        print("dunhill : ", cigar["dunhill"].Value())

        print("---- DRINK ----")
        print("water : ", drink["water"].Value())
        print("tea : ", drink["tea"].Value())
        print("beer : ", drink["beer"].Value())
        print("milk : ", drink["milk"].Value())
        print("coffee : ", drink["coffee"].Value())

        print("---- NATION ----")
        print("german : ", nation["german"].Value())
        print("norwegian : ", nation["norwegian"].Value())
        print("swede : ", nation["swede"].Value())
        print("brit : ", nation["brit"].Value())
        print("dane : ", nation["dane"].Value())
        
        print("Number of solutions:", count)

if __name__ == '__main__':
    main()
