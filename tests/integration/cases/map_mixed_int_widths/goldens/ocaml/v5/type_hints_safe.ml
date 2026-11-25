module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("a", OInt 1);
    ("b", OInt 1099511627776)
]

end
