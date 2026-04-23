module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("lint", OList [OInt 2; OList [OInt 1]]);
    ("test", OList [OInt 5; OList [OInt 7]])
]

end
