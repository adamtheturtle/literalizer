module Main

type Val =
    | FStr of string
    | FSet of Val list
let my_data: Val = FSet [
    // before apple
    FStr "apple";
    FStr "banana"  // banana inline
    // trailing
]
