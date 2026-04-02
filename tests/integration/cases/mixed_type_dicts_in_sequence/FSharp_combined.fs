module Check

type Val =
    | FBool of bool
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let mutable my_data: Val = FList [
    FMap [("type", FStr "create"); ("pr_id", FStr "pr_1"); ("draft", FBool true)];
    FMap [("type", FStr "create"); ("pr_id", FStr "pr_2")]
]
