module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let private _mainDeclaration () =
    let mutable my_data: Val = FMap [
        ("level1", FMap [("level2", FMap [("level3", FMap [("level4", FMap [("value", FStr "deep"); ("items", FList [FStr "a"; FStr "b"])])]); ("sibling", FInt 42L)]); ("tags", FList [FMap [("name", FStr "tag1"); ("meta", FMap [("priority", FInt 1L); ("labels", FList [FStr "x"; FStr "y"])])]])])
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FMap [
        ("level1", FMap [("level2", FMap [("level3", FMap [("level4", FMap [("value", FStr "deep"); ("items", FList [FStr "a"; FStr "b"])])]); ("sibling", FInt 42L)]); ("tags", FList [FMap [("name", FStr "tag1"); ("meta", FMap [("priority", FInt 1L); ("labels", FList [FStr "x"; FStr "y"])])]])])
    ]
    ignore my_data
