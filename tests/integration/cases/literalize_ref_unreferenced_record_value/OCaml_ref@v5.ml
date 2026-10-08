module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OMap of (string * val_t) list
let other : val_t = OStr "true"
let my_data : val_t = OMap [
    ("main", OMap [("x", OInt 1); ("y", OStr "s")])
]

end
