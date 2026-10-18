module Check = struct

type val_t =
  | OStr of string
  | OInt of int
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("within_i32", OInt 1705320000);
    ("beyond_i32", OInt 4085195400)
]

end
