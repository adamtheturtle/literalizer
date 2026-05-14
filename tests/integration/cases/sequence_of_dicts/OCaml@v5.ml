module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OList [
    OMap [("name", OStr "Alice"); ("age", OInt 30)];
    OMap [("name", OStr "Bob"); ("age", OInt 25)]
]

end
