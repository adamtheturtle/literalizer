module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
let private _mainDeclaration () =
    let mutable my_data: Val = FList [
        FInt 1L;
        FStr "email";
        FStr "a@gmail.com";
        FInt 100L
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FList [
        FInt 1L;
        FStr "email";
        FStr "a@gmail.com";
        FInt 100L
    ]
    ignore my_data
