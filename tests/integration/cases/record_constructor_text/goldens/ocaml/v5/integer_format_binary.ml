module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("text", OStr "Record0(");
    ("number", OInt 0b1)
]

end
