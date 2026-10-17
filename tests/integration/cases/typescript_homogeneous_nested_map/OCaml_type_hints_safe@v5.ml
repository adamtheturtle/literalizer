module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("first", OMap [("x", OInt 1); ("y", OInt 2)]);
    ("second", OMap [("z", OInt 3)])
]

end
