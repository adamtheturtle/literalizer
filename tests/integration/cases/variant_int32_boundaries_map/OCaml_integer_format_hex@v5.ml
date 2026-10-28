module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("below", OInt (-0x80000001));
    ("minimum", OInt (-0x80000000));
    ("above", OInt (-0x7fffffff));
    ("nested", OList [OInt 0x0])
]

end
