module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("below", OInt (-2147483649));
    ("minimum", OInt (-2147483648));
    ("above", OInt (-2147483647));
    ("nested", OList [OInt 0])
]

end
