module Check = struct

type val_t =
  | ONull
  | OBool of bool
  | OInt of int
  | OStr of string
  | ODate of (int * int * int)
  | ODatetime of ((int * int * int) * (int * int * int))
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("name", OStr "Alice");
    ("age", OInt 30);
    ("active", OBool true);
    ("score", ONull);
    ("joined", ODate (2024, 1, 15));
    ("last_login", ODatetime ((2024, 1, 15), (12, 30, 0)));
    ("avatar", OStr "48656c6c6f")
]

end
