module Check = struct

type val_t =
  | OStr of string
  | OInt of int
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("ts", OInt 32535215999)
]

end
