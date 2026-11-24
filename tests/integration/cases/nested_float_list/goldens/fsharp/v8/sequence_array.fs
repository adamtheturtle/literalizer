module Main

type Val =
    | FFloat of float
    | FList of Val array
let my_data: Val array = [|
    FList ([|FFloat 1.5; FFloat 2.5|]);
    FList ([|FFloat 3.5; FFloat 4.5|])
|]
