module Check = struct

type val_t =
  | OBool of bool
  | OInt of int
  | OStr of string
  | OMap of (string * val_t) list
  | OSet of val_t list
let my_data : val_t = OMap [
    ("name", OStr "Alice");
    ("tags", OSet [OBool true; OInt 42; OStr "apple"])
]

end
