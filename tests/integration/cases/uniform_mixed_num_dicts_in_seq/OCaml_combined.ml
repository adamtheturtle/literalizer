module Check = struct

type val_t =
  | OInt of int
  | OFloat of float
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OList [
    OMap [("x", OInt 1); ("y", OFloat 2.5)];
    OMap [("x", OInt 3); ("y", OFloat 4.0)]
]

end
