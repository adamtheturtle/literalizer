module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("first", OMap [("items", OList [OInt 1; OMap [("value", OInt 2)]])]);
    ("second", OMap [("items", OList [OInt 1; OMap [("value", OStr "s")]])])
]

end
