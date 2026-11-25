module Check = struct

type val_t =
  | ONull
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("nil", OList [OList [OList [OList [OList [OList [OList [OList [OList [ONull]]]]]]]]]);
    ("empty", OList [OList [OList [OList [OList [OList [OList [OList [OList [OList []]]]]]]]]]);
    ("siblings", OList [OList [OList [OList [OList [OList [OList [OList [OList [OList [OInt 4; OInt 5]]]]]]]]]])
]

end
