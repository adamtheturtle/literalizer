module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
let private _mainDeclaration () =
    let mutable my_data: Val = FList [
        FList [FInt 2L; FStr "hello"];  // trailing note
        // next element
        FList [FInt 3L; FStr "world"]
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FList [
        FList [FInt 2L; FStr "hello"];  // trailing note
        // next element
        FList [FInt 3L; FStr "world"]
    ]
    ignore my_data
