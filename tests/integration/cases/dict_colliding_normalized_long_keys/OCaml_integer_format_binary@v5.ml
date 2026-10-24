module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("a_b", OInt 0b1);
    ("a-b", OInt 0b10);
    ("averyveryverylongkeynamethatgoesonandonandon", OInt 0b11);
    ("averyveryverylongkeynamethatgoesonandmore", OInt 0b100)
]

end
