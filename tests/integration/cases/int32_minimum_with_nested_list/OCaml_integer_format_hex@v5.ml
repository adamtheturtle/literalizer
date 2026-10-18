module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("minimum", OInt (-0x80000000));
    ("neighbor", OInt (-0x7fffffff));
    ("maximum", OInt 0x7fffffff);
    ("nested", OList [OInt (-0x80000000)])
]

end
