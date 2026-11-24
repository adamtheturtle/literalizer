module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("a_b", OInt 0x1);
    ("a-b", OInt 0x2);
    ("averyveryverylongkeynamethatgoesonandonandon", OInt 0x3);
    ("averyveryverylongkeynamethatgoesonandmore", OInt 0x4)
]

end
