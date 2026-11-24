module Check = struct

type val_t =
  | OFloat of float
  | OStr of string
  | OMap of (string * val_t) list
let std : val_t = OMap [
    ("nan", OFloat nan);
    ("positive", OFloat infinity);
    ("negative", OFloat neg_infinity)
]

end
