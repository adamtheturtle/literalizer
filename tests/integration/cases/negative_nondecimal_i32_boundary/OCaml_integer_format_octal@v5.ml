module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("minimum", OInt (-0o20000000000));
    ("below", OInt (-0o26264057000))
]

end
