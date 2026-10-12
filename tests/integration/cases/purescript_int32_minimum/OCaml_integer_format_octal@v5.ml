module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("minimum", OInt (-0o20000000000));
    ("neighbor", OInt (-0o17777777777));
    ("maximum", OInt 0o17777777777);
    ("nested", OList [OInt (-0o20000000000)])
]

end
