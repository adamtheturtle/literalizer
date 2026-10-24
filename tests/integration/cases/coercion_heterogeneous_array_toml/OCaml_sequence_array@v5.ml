module Check = struct

type val_t =
  | OInt of int
  | OFloat of float
  | OStr of string
  | OArray of val_t array
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("_", OArray [|OInt 1; OFloat 2.5; OInt 3|])
]

end
