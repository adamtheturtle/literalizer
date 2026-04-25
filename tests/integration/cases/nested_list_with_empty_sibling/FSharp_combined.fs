module Check

type Val =
    | FInt of int64
    | FList of Val list
let private _checkDeclaration () =
    let mutable my_data: Val = FList [
        FList [FInt 1L; FInt 2L];
        FList [];
        FList [FInt 3L; FInt 4L]
    ]
    ignore my_data

let private _checkAssignment () =
    let my_data: Val = FList [
        FList [FInt 1L; FInt 2L];
        FList [];
        FList [FInt 3L; FInt 4L]
    ]
    ignore my_data
