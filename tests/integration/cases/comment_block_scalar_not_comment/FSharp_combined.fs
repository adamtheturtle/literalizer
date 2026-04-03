module Check

type Val =
    | FStr of string
    | FMap of (string * Val) list
let mutable my_data: Val = FMap [
    ("description", FStr "# not a comment\n");
    ("name", FStr "foo")
]
