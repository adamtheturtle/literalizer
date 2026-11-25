module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let private _mainDeclaration () =
    let mutable my_data: Val = FMap [
        ("omap_value", FMap [("first", FInt 1L)]);
        ("sibling_lists", FMap [("numbers", FList [FInt 1L; FInt 2L]); ("strings", FList [FStr "x"; FStr "y"])]);
        ("ref_marker_present", FList [FStr "$keep"; FStr "z"])
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FMap [
        ("omap_value", FMap [("first", FInt 1L)]);
        ("sibling_lists", FMap [("numbers", FList [FInt 1L; FInt 2L]); ("strings", FList [FStr "x"; FStr "y"])]);
        ("ref_marker_present", FList [FStr "$keep"; FStr "z"])
    ]
    ignore my_data
