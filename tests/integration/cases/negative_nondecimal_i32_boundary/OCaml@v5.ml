module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("minimum", OInt (-2147483648));
    ("below", OInt (-3000000000))
]

end
