module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("below", OInt (-0b10000000000000000000000000000001));
    ("minimum", OInt (-0b10000000000000000000000000000000));
    ("above", OInt (-0b1111111111111111111111111111111));
    ("nested", OList [OInt 0b0])
]

end
