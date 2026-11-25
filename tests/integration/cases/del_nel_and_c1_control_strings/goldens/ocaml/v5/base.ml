module Check = struct

type val_t =
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("del", OStr "ab");
    ("nel", OStr "ab");
    ("c1", OStr "ab")
]

end
