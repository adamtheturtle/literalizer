type Val =
    | FNull
    | FBool of bool
    | FInt of int64
    | FFloat of float
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
    | FSet of Val list
    | FDate of System.DateTime
    | FDatetime of System.DateTime

let my_data: Val = FMap [
    ("level1", FMap [("level2", FMap [("level3", FMap [("level4", FMap [("value", FStr "deep"); ("items", FList [FStr "a"; FStr "b"])])]); ("sibling", FInt 42L)]); ("tags", FList [FMap [("name", FStr "tag1"); ("meta", FMap [("priority", FInt 1L); ("labels", FList [FStr "x"; FStr "y"])])]])])
]
