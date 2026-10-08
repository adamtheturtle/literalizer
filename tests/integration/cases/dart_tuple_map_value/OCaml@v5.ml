module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("rows", OList [OMap [("x", OInt 1); ("y", OStr "a")]; OMap [("x", OInt 2); ("y", OStr "b")]])
]

end
