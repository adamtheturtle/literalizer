module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("numbers", OList [OInt 1; OInt 2]);
    ("nested", OMap [("inner", OList [OInt 3])]);
    ("mixed", OList [OInt 4; OStr "five"])
]

end
