module Main

type Val =
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FList [
    FList [
        FMap [("item", FStr "existing")];
        FStr "kept"
        // This comment trails the first pair.
    ];
    FList [FMap [("item", FStr "next")]; FStr "also kept"];
    // This comment describes the last pair.
    FList [FMap [("item", FStr "last")]; FStr "kept too"]
]
