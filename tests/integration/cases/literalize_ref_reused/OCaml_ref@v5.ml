module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let shared_var : val_t = OMap [
    ("_", OStr "_")
]
let my_data : val_t = OList [
    shared_var;
    shared_var
]

end
