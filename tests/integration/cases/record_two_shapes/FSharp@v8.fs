module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("user", FMap [("id", FInt 1L); ("name", FStr "Alice")]);
    ("project", FMap [("title", FStr "report"); ("tags", FList [FStr "draft"; FStr "urgent"])])
]
