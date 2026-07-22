module Main

type Val =
    | FNull
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let private _mainDeclaration () =
    let mutable my_data: Val = FMap [
        ("rows", FList [FMap [("replacement", FNull); ("present", FInt 1L)]; FMap [("replacement", FInt 2L); ("present", FInt 3L)]])
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FMap [
        ("rows", FList [FMap [("replacement", FNull); ("present", FInt 1L)]; FMap [("replacement", FInt 2L); ("present", FInt 3L)]])
    ]
    ignore my_data
