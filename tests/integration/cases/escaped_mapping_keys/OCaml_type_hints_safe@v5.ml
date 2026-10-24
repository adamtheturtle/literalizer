module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("quote\"backslash\\", OInt 1);
    ("line\nbreak", OInt 2);
    ("$(literal)${text}", OInt 3);
    ("RStr prefix", OInt 4)
]

end
