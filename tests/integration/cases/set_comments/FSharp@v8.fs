module Main

type Val =
    | FStr of string
    | FSet of Val list
let my_data: Val = FSet [
    FStr "apple";  // inline comment
    // before banana
    FStr "banana"
    // trailing
]
