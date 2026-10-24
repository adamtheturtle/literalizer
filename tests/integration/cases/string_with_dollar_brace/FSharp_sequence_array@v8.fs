module Main

type Val =
    | FStr of string
    | FList of Val array
let my_data: Val array = [|
    FStr "prefix ${HOME} suffix";
    FStr "${interpolated}"
|]
