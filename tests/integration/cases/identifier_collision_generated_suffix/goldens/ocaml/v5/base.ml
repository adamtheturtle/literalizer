module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("a-b", OInt 1);
    ("a b", OInt 2);
    ("a-b-2", OInt 3)
]

end
