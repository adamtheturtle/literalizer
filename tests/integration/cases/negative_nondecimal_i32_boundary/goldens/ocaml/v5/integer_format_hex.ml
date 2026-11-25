module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("minimum", OInt (-0x80000000));
    ("below", OInt (-0xb2d05e00))
]

end
