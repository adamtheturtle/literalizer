module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("b", OMap [("k", OInt 1)]);
    ("a", OMap [("k", OInt 2208988800)])
]

end
