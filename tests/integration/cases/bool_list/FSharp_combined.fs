module Check

type Val =
    | FBool of bool
    | FList of Val list
let private _checkDeclaration () =
    let mutable my_data: Val = FList [
        FBool true;
        FBool false;
        FBool true
    ]
    ignore my_data

let private _checkAssignment () =
    let my_data: Val = FList [
        FBool true;
        FBool false;
        FBool true
    ]
    ignore my_data
