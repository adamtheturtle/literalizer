module Check = struct

type val_t =
  | OBool of bool
  | OInt of int
  | OFloat of float
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("name", OStr "Alice");
    ("age", OInt 30);
    ("active", OBool true);
    ("score", OFloat 4.5)
]

end
