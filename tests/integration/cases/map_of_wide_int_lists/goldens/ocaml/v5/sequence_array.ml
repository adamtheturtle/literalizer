module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OArray of val_t array
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("a", OArray [|OInt 4294967296; OInt 4294967297|])
]

end
