module Check

type Val =
    | FBool of bool
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
type MType_() =
    member _.Op(_operation: obj) : obj = null
let m = MType_()
m.Op(FMap [("type", FStr "create"); ("pr_id", FStr "pr_1"); ("draft", FBool true)])
m.Op(FMap [("type", FStr "create"); ("pr_id", FStr "pr_2")])
