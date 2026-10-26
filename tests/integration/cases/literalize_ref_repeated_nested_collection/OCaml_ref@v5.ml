module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let shared : val_t = OList [
    OList [OInt 1; OInt 2];
    OMap [("value", OInt 1)]
]
let my_data : val_t = OList [
    shared;
    shared
]

end
