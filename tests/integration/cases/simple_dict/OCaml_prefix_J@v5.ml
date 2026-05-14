module Check = struct

type val_t =
  | JNull
  | JBool of bool
  | JInt of int
  | JStr of string
  | JMap of (string * val_t) list
let my_data : val_t = JMap [
    ("name", JStr "Alice");
    ("age", JInt 30);
    ("active", JBool true);
    ("score", JNull)
]

end
