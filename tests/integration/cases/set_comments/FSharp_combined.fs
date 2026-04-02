module Check

type Val =
    | FStr of string
    | FSet of Val list
let mutable my_data: Val = FSet [
    FStr "apple";  // inline comment
    // before banana
    FStr "banana"
    // trailing
]
