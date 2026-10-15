module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FMap [
    //
    // document heading
    // before the first entry
    // after the key
    // before the value
    ("counts", FList [
        // before the first item
        FInt 1L;  // inline block after the comma
        // before the second item
        FInt 2L
        // trailing inside the array
    ]);  // after the nested collection
    ("more", FList [
        FInt 3L;
        //
        // block heading
        // block continuation
        FInt 4L  // final inline
    ])
    // trailing inside the object
    // after the root
    // after the document
]
