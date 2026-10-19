module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("first", OList [OList [OInt 1; OStr "value"]; OList []]);
    ("second", OList [OList []; OList [OInt 2; OStr "other"]])
]

end
