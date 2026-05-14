module Check = struct

type val_t =
  | ONull
  | OBool of bool
  | OInt of int
  | OFloat of float
  | OStr of string
  | ODate of (int * int * int)
  | ODatetime of ((int * int * int) * (int * int * int))
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("s", OStr "string");
    ("i", OInt 1);
    ("f", OFloat 1.5);
    ("b", OBool true);
    ("n", ONull);
    ("d", ODate (2024, 1, 15));
    ("dt", ODatetime ((2024, 1, 15), (12, 0, 0)));
    ("by", OStr "48656c6c6f")
]

end
