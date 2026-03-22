type val_t =
  | ONull
  | OBool of bool
  | OInt of int
  | OFloat of float
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
  | OSet of val_t list
module Check = struct

let x : val_t = OList [
    OMap [("name", OStr "Alice"); ("age", OInt 30)];
    OMap [("name", OStr "Bob"); ("age", OInt 25)]
]

end
