module Main

type Val =
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let process (_value: obj) : obj = null
// Test cases
process(FMap [("type", FStr "create"); ("pr_id", FStr "pr_1")])  // first case
process(FMap [("type", FStr "update"); ("pr_id", FStr "pr_2")])  // second case
// third case
process(FMap [("type", FStr "delete"); ("pr_id", FStr "pr_3")])
