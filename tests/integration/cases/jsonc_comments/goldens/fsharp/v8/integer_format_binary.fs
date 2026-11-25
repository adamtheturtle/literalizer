module Main

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    // A JSONC input case with both comment forms.
    ("url", FStr "https://example.org/a/*b*/");  // detail
    // continued
    ("count", FInt 0b10L)  // trailing line comment
]
