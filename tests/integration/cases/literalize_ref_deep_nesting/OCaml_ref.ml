module Check = struct

type val_t =
  | OStr of string
  | OMap of (string * val_t) list
let deep : val_t = OMap [
    ("_", OStr "_")
]
let my_data : val_t = OMap [
    ("a", OMap [("b", OMap [("c", deep)])])
]

end
