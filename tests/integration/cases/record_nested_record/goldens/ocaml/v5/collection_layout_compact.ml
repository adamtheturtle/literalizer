module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("id", OInt 1);
    ("owner", OMap [("name", OStr "Alice"); ("age", OInt 30)])
]

end
