module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("astral", FStr "😀");
    ("mixed", FStr "a😀b");
    ("count", FInt 2L);
    ("list", FList [FStr "😀"; FInt 1L]);
    ("nested", FMap [("inner", FStr "😀")])
]
