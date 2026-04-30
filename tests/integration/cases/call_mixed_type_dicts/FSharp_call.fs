module Main

type Val =
    | FBool of bool
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
type MgrType_() =
    member _.run(_operation: obj) : obj = null
type AppType_() =
    member _.mgr = MgrType_()
let app = AppType_()
app.mgr.run(FMap [("type", FStr "create"); ("pr_id", FStr "pr_1"); ("draft", FBool true)])
app.mgr.run(FMap [("type", FStr "create"); ("pr_id", FStr "pr_2")])
