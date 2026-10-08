module Check = struct

type val_t =
  | OBool of bool
  | OInt of int
  | OFloat of float
  | OStr of string
  | OArray of val_t array
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("d", OArray [|OMap [("a", OArray [|OMap [("b", OArray [|OInt 1; OArray [|OFloat 2.5; OArray [|OStr "x"; OArray [|OBool true|]|]|]|])]|])]|])
]

end
