module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("a", OList [OList [OInt 1; OInt 2]]);
    ("b", OList [OList [OInt 3]])
]

end
