module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("minimum", OInt (-0b10000000000000000000000000000000));
    ("below", OInt (-0b10110010110100000101111000000000))
]

end
