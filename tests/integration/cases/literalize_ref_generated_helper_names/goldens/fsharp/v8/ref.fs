module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let std: Val = FMap [
    ("a", FInt 1L)
]
let arena: Val = FMap [
    ("a", FInt 1L)
]
let allocator: Val = FMap [
    ("a", FInt 1L)
]
let my_data: Val = FList [
    std;
    arena;
    allocator
]
