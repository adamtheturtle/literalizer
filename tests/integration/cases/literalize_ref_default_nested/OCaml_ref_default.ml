module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_var : val_t = OMap [
    ("_", OStr "_")
]
let item_var : val_t = OMap [
    ("_", OStr "_")
]
let my_data : val_t = OMap [
    ("key", my_var);
    ("items", OList [item_var; OMap [("fallback", OStr "value")]])
]

end
