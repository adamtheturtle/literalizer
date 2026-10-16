module Check = struct

type val_t =
  | ONull
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OList [
    OList [OMap [("a", OInt 1)]; OMap [("a", ONull)]; OInt 42];
    OList [OMap [("a", OInt 1)]; OMap [("a", OStr "s")]; OInt 42];
    OList [OMap [("a", OInt 1)]; OMap [("a", ONull)]];
    OList [OMap [("a", OInt 1)]; OMap [("a", OStr "s")]]
]

end
