module Check

type Val =
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let mutable my_data: Val = FMap [
    ("users", FList [FMap [("name", FStr "Bob"); ("tags", FList [FStr "admin"; FStr "user"])]; FMap [("name", FStr "Carol"); ("tags", FList [FStr "guest"])]])
]
