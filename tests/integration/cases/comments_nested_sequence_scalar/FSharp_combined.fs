module Main

type Val =
    | FStr of string
    | FList of Val list
let private _mainDeclaration () =
    let mutable my_data: Val = FList [
        FList [FStr "ADD"; FStr "alice"; FStr "hello"];
        FList [FStr "DEL"; FStr "bob"; FStr "5"]  // removes "world"
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FList [
        FList [FStr "ADD"; FStr "alice"; FStr "hello"];
        FList [FStr "DEL"; FStr "bob"; FStr "5"]  // removes "world"
    ]
    ignore my_data
