module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("a_b", OInt 0o1);
    ("a-b", OInt 0o2);
    ("averyveryverylongkeynamethatgoesonandonandon", OInt 0o3);
    ("averyveryverylongkeynamethatgoesonandmore", OInt 0o4)
]

end
