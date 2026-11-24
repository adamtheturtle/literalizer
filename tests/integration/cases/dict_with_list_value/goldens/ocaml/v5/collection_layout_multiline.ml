module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("name", OStr "Alice");
    ("scores", OList [
        OInt 10;
        OInt 20;
        OInt 30
    ])
]

end
