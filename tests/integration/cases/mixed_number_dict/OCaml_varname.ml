module Check = struct

type val_t =
  | ONull
  | OBool of bool
  | OInt of int
  | OFloat of float
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
  | OSet of val_t list

let my_data : val_t = OMap [
    ("a", OInt 1);
    ("b", OFloat 2.5);
    ("c", OInt 3)
]

end
