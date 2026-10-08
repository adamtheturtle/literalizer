module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("url", OStr "https://example.org/a/*b*/");
    ("count", OInt 2)
]

end
