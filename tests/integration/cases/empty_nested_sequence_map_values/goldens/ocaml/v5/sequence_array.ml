module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OArray of val_t array
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("alpha", OArray [|OInt 2; OArray [||]|]);
    ("beta", OArray [|OInt 5; OArray [|OStr "x"|]|])
]

end
