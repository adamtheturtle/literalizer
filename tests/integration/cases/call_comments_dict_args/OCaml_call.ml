module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let process _ = ()
(* Test cases *)
let _ = process(OMap [("type", OStr "create"); ("pr_id", OStr "pr_1")])  (* first case *)
let _ = process(OMap [("type", OStr "update"); ("pr_id", OStr "pr_2")])  (* second case *)
(* third case *)
let _ = process(OMap [("type", OStr "delete"); ("pr_id", OStr "pr_3")])

end
