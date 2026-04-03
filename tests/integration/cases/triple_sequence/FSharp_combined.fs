module Check

type Val =
    | FBool of bool
    | FInt of int64
    | FStr of string
    | FList of Val list
let private _checkDeclaration () =
    let mutable my_data: Val = FList [
        FInt 1L;
        FStr "hello";
        FBool true
    ]
    ignore my_data

let private _checkAssignment () =
    let my_data: Val = FList [
        FInt 1L;
        FStr "hello";
        FBool true
    ]
    ignore my_data
