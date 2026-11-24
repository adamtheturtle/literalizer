module Check = struct

type val_t =
  | OBool of bool
  | OInt of int
  | OStr of string
  | OArray of val_t array
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("h", OArray [|OInt 1; OStr "a"; OArray [|OInt 2; OStr "b"|]; OMap [("k", OArray [|OBool true|])]|])
]

end
