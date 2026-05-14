module Check = struct

type val_t =
  | ONull
  | OInt of int
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("outer", OMap [("a", OInt 1); ("b", OStr "x"); ("c", ONull)])
]

end
