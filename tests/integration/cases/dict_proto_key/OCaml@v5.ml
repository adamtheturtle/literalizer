module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("__proto__", OMap [("x", OInt 1)]);
    ("n", OMap [("__proto__", OInt 3)]);
    ("y", OInt 2)
]

end
