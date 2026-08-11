module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("a_b", OInt 1);
    ("a-b", OInt 2);
    ("averyveryverylongkeynamethatgoesonandonandon", OInt 3);
    ("averyveryverylongkeynamethatgoesonandmore", OInt 4)
]

end
