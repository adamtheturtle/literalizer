module Check = struct

type val_t =
  | OBool of bool
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("project", OStr "alpha");
    ("lead_task", OMap [("id", OInt 100); ("description", OStr "first task"); ("is_done", OBool false); ("blocks", OList [OInt 102; OInt 103])])
]

end
