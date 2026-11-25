module Check = struct

type json_t =
  | ONull
  | OBool of bool
  | OInt of int
  | OStr of string
  | OMap of (string * json_t) list
let my_data : json_t = OMap [
    ("name", OStr "Alice");
    ("age", OInt 30);
    ("active", OBool true);
    ("score", ONull)
]

end
