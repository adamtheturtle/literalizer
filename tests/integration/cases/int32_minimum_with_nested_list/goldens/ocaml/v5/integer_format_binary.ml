module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("minimum", OInt (-0b10000000000000000000000000000000));
    ("neighbor", OInt (-0b1111111111111111111111111111111));
    ("maximum", OInt 0b1111111111111111111111111111111);
    ("nested", OList [OInt (-0b10000000000000000000000000000000)])
]

end
