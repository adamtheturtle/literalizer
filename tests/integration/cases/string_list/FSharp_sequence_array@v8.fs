module Main

type Val =
    | FStr of string
    | FList of Val array
let my_data: Val array = [|
    FStr "foo";
    FStr "bar";
    FStr "baz"
|]
