% vim: ft=prolog

% Define a predicate to select food items based on type and subtype
select_foods(Type, Subtypes, Options) :-
    % Use findall to gather all food items that match the type and subtypes.
    findall(Food, (food(Type, Subtype, Food, _, _),
                   member(Subtype, Subtypes)),
            Options).

% Define a predicate to get the total calories of a list of food items
sum_calories([], 0).
sum_calories([Food|Foods], Calories) :-
    % Retrieve the calories of the current food item.
    food(_, _, Food, Calories1, _),
    % Recursively sum the calories of the remaining food items.
    sum_calories(Foods, Calories2),
    % Calculate the total calories.
    Calories is Calories1 + Calories2.

% Define a predicate to get the total price of a list of food items
sum_price([], 0).
sum_price([Food|Foods], Price) :-
    % Retrieve the price of the current food item.
    food(_, _, Food, _, Price1),
    % Recursively sum the prices of the remaining food items.
    sum_price(Foods, Price2),
    % Calculate the total price.
    Price is Price1 + Price2.

% Define a predicate to generate all combinations of a list with a specified count
combination(_, 0, []).
combination([H|T], N, [H|Combination]) :-
    % Construct a combination by adding the current element to the list.
    N > 0,
    N1 is N - 1,
    combination([H|T], N1, Combination).
combination([_|T], N, Combination) :-
    % Skip the current element and continue generating the combination.
    N > 0,
    combination(T, N, Combination).

% Define a predicate to generate a menu based on food items, their counts, and calorie constraints
generate_dishes(F1, N1, F2, N2, F3, N3, F4, N4, MaxCalories, Menu) :-
    % Generate all possible combinations of food items based on their counts.
    findall(Combo, (
        combination(F1, N1, C1),
        combination(F2, N2, C2),
        combination(F3, N3, C3),
        combination(F4, N4, C4),
        % Concatenate the combinations of all food types.
        append(C1, C2, Temp1),
        append(Temp1, C3, Temp2),
        append(Temp2, C4, Combo)
    ), AllCombos),
    
    % Filter the combinations based on calorie constraints.
    findall(Combo, (
        member(Combo, AllCombos),
        % Calculate the total calories of the combination.
        sum_calories(Combo, Calories),
        % Check if the total calories are within the specified limit.
        Calories =< MaxCalories
    ), Menu).

% Define a predicate to generate a menu based on type, subtype, counts, calorie constraints, and price
get_menu(T1, ST1, N1, T2, ST2, N2, T3, ST3, N3, T4, ST4, N4, MaxCalories, Menu) :-
    % Select food items based on type and subtypes.
    select_foods(T1, ST1, F1), 
    select_foods(T2, ST2, F2), 
    select_foods(T3, ST3, F3), 
    select_foods(T4, ST4, F4), 
    % Generate all possible menu combinations based on selected food items and counts.
    generate_dishes(F1, N1, F2, N2, F3, N3, F4, N4, MaxCalories, NoPriceMenu),
    % Add the price to the Dish items by calculating the total price for each combination.
    findall((Dish, Price), (
        member(Dish, NoPriceMenu),
        sum_price(Dish, Price)
    ), Menu).
