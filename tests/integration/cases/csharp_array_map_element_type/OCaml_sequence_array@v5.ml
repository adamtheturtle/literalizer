module Check = struct

type val_t =
  | OBool of bool
  | OInt of int
  | OFloat of float
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("d", [|OMap [("a", [|OMap [("b", [|OInt 1; [|OFloat 2.5; [|OStr "x"; [|OBool true|]|]|]|])]|])]|])
]

end
