module Main

type Val =
    | FNull
    | FBool of bool
    | FInt of int64
    | FStr of string
    | FList of Val list
let private _mainDeclaration () =
    let mutable my_data: Val = FList [
        FInt 1L;
        FStr "hello";
        FBool true;
        FNull
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FList [
        FInt 1L;
        FStr "hello";
        FBool true;
        FNull
    ]
    ignore my_data
