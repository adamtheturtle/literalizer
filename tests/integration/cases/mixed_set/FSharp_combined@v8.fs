module Main

type Val =
    | FBool of bool
    | FInt of int64
    | FStr of string
    | FSet of Val list
let private _mainDeclaration () =
    let mutable my_data: Val = FSet [
        FBool true;
        FInt 42L;
        FStr "apple"
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FSet [
        FBool true;
        FInt 42L;
        FStr "apple"
    ]
    ignore my_data
