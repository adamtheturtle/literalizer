module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("if", OInt 1);
    ("then", OInt 2);
    ("else", OInt 3);
    ("let", OInt 4);
    ("in", OInt 5);
    ("using", OInt 6);
    ("missing", OInt 7);
    ("assert", OInt 8);
    ("as", OInt 9);
    ("Infinity", OInt 10);
    ("NaN", OInt 11);
    ("merge", OInt 12);
    ("Some", OInt 13);
    ("toMap", OInt 14);
    ("forall", OInt 15);
    ("with", OInt 16);
    ("ordinary", OInt 17)
]

end
