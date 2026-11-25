module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("metrics", OMap [("count", OInt 100); ("rate", OInt 50)]);
    ("flags", OMap [("retries", OInt 3); ("timeout", OInt 30)])
]

end
