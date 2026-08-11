module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let foo : val_t = OMap [
    ("_", OStr "_")
]
let my_data : val_t = OMap [
    ("mapping", OMap [("value", foo)]);
    ("items", OList [OMap [("other", OInt 1)]; foo])
]

end
