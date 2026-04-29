datatype val_t =
    SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
fun process _ = ()
(* Test cases *)
val _ = process(SMap [("type", SStr "create"), ("pr_id", SStr "pr_1")])  (* first case *)
val _ = process(SMap [("type", SStr "update"), ("pr_id", SStr "pr_2")])  (* second case *)
(* third case *)
val _ = process(SMap [("type", SStr "delete"), ("pr_id", SStr "pr_3")])
