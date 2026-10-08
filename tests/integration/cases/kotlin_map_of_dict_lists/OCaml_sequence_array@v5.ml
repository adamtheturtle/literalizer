module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("a", [|OMap [("k", OInt 1)]|]);
    ("b", [|OMap [("k", OInt 2)]|])
]

end
