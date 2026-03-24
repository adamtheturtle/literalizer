type val_t =
  | ONull
  | OBool of bool
  | OInt of int
  | OFloat of float
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
  | OSet of val_t list
  | ODate of (int * int * int)
  | ODatetime of ((int * int * int) * (int * int * int))
module Check = struct

let my_data : val_t = OMap [
    ("name", OStr "Alice");
    ("score", ONull);
    ("age", OInt 30)
]

end
