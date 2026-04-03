module Check

type Val =
    | FBool of bool
    | FInt of int64
    | FStr of string
    | FSet of Val list
let private _checkDeclaration () =
    let mutable my_data: Val = FSet [
        FBool true;
        FInt 42L;
        FStr "apple"
    ]
    ignore my_data

let private _checkAssignment () =
    let my_data: Val = FSet [
        FBool true;
        FInt 42L;
        FStr "apple"
    ]
    ignore my_data
