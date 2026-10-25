module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("lists", OList [OList [OInt 1]; OList [OStr "x"]; OList []]);
    ("maps", OList [OMap [("x", OInt 1)]; OMap [("x", OStr "s")]]);
    ("empties", OMap [("a", OList [OInt 1]); ("b", OList [])])
]

end
