module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OMap of (string * val_t) list
let my_var : val_t = OInt 1
let my_data : val_t = OMap [
    ("key", my_var)
]

end
