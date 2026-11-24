module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OMap of (string * val_t) list
let bound : val_t = OInt 2
let my_data : val_t = OMap [
    ("value", bound)
]

end
