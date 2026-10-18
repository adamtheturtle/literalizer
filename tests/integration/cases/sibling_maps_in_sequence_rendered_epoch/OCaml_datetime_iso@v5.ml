module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OList [
    OMap [("k", OStr "2040-01-01T00:00:00+00:00")];
    OMap [("k", OInt 1)]
]

end
