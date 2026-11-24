module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("lower", OInt 3735928559);
    ("upper", OInt 31);
    ("negative", OInt (-16));
    ("zero", OInt 0)
]

end
