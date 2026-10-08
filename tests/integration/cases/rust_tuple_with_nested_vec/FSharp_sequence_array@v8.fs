module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("lint", [|FInt 2L; [||]|]);
    ("test", [|FInt 5L; [|FStr "compile"|]|]);
    ("package", [|FInt 7L; [|FStr "link"; FStr "test"|]|])
]
