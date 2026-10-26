module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OList [
    OMap [("input", OMap [("name", OStr "alice"); ("city", OStr "paris")]); ("expected", OMap [("count", OInt 1); ("total", OInt 2)])];
    OMap [("input", OMap [("name", OInt 10); ("city", OInt 20)]); ("expected", OMap [("count", OStr "done"); ("total", OStr "pending")])]
]

end
