structure Check = struct

datatype val_t =
    SBool of bool
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
structure app = struct
structure mgr = struct
fun op _ = ()
end
end
app.mgr.op(SMap [("type", SStr "create"), ("pr_id", SStr "pr_1"), ("draft", SBool true)])
app.mgr.op(SMap [("type", SStr "create"), ("pr_id", SStr "pr_2")])

end
