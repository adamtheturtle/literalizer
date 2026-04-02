module Check

type Val =
    | FStr of string
    | FList of Val list
let mutable my_data: Val = FList [
    FStr "foo";
    FStr "bar";
    FStr "baz"
]
