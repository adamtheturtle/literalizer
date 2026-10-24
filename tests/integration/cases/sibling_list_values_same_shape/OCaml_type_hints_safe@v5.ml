module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("test", OList [OInt 5; OList [OStr "compile"; OStr "test"]]);
    ("package", OList [OInt 7; OList [OStr "link"; OStr "test"]])
]

end
