module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("assert", OInt 1);
    ("else", OInt 1);
    ("error", OInt 1);
    ("false", OInt 1);
    ("for", OInt 1);
    ("function", OInt 1);
    ("if", OInt 1);
    ("import", OInt 1);
    ("importbin", OInt 1);
    ("importstr", OInt 1);
    ("in", OInt 1);
    ("local", OInt 1);
    ("null", OInt 1);
    ("self", OInt 1);
    ("super", OInt 1);
    ("tailstrict", OInt 1);
    ("then", OInt 1);
    ("true", OInt 1);
    ("ordinary", OInt 1)
]

end
