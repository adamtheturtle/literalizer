module Check = struct

type val_t =
  | OBool of bool
  | OInt of int
  | OStr of string
let my_data : val_t = OMap [
    ("name", OStr "Alice");
    ("age", OInt 30);
    ("active", OBool true)
]

end
