module Check

type Val =
    | FStr of string
    | FList of Val list
let mutable my_data: Val = FList [
    // line 1
    // line 2
    FStr "a"
]
