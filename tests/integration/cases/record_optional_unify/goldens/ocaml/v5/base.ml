module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("items", OList [OMap [("id", OInt 1)]; OMap [("id", OInt 2); ("count", OInt 10)]; OMap [("id", OInt 3); ("count", OInt 20)]])
]

end
