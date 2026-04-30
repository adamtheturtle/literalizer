module Check = struct

type val_t =
  | OBool of bool
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
module App = struct
module Mgr = struct
let run _ = ()
end
end
let _ = App.Mgr.run(OMap [("type", OStr "create"); ("pr_id", OStr "pr_1"); ("draft", OBool true)])
let _ = App.Mgr.run(OMap [("type", OStr "create"); ("pr_id", OStr "pr_2")])

end
