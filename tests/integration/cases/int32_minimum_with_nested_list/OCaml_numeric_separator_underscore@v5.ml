module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("minimum", OInt (-2_147_483_648));
    ("neighbor", OInt (-2_147_483_647));
    ("maximum", OInt 2_147_483_647);
    ("nested", OList [OInt (-2_147_483_648)])
]

end
