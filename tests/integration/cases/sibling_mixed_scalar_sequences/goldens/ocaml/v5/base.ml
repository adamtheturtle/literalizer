module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("left", OList [OInt 1; OStr "one"]);
    ("right", OList [OInt 2; OStr "two"])
]

end
