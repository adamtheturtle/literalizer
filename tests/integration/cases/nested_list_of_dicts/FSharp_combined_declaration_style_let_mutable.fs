module Check

type Val =
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let mutable my_data: Val = FList [
    FList [FMap [("name", FStr "Alice")]; FMap [("name", FStr "Bob")]];
    FList [FMap [("name", FStr "Charlie")]; FMap [("name", FStr "Dave")]]
]
