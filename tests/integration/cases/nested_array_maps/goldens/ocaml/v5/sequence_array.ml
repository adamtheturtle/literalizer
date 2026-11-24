module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OArray of val_t array
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("groups", OArray [|OArray [|OMap [("id", OInt 1)]|]; OArray [|OMap [("id", OInt 2)]|]|])
]

end
