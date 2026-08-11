module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let consume (_items: obj, _mapping: obj) : obj = null
let foo: Val = FInt 42L
consume(FList [
    FMap [
        ("other", FInt 1L)
    ];
    foo
], FMap [
    ("left", foo);
    ("other", FInt 1L)
])
