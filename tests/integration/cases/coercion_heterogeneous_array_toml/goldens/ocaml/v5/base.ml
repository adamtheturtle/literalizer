module Check = struct

type val_t =
  | OInt of int
  | OFloat of float
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("_", OList [OInt 1; OFloat 2.5; OInt 3])
]

end
