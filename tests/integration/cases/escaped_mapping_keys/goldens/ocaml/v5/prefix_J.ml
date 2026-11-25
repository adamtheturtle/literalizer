module Check = struct

type val_t =
  | JInt of int
  | JStr of string
  | JMap of (string * val_t) list
let my_data : val_t = JMap [
    ("quote\"backslash\\", JInt 1);
    ("line\nbreak", JInt 2);
    ("$(literal)${text}", JInt 3);
    ("RStr prefix", JInt 4)
]

end
