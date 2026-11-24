module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let existing : val_t = OInt 1
let my_data : val_t = OMap [
    ("nested", OList [OInt 0; existing])
]

end
