module Check = struct

type val_t =
  | OStr of string
  | ODate of (int * int * int)
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("a", OMap [("k", ODate (2020, 1, 1))]);
    ("b", OMap [("k", OStr "string")])
]

end
