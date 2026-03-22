module Check = struct

type val_t =
  | ONull
  | OBool of bool
  | OInt of int
  | OFloat of float
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
  | OSet of val_t list

let my_data : val_t = OList [
    OMap [("key", OStr "hello   world"); ("value", OInt 1)]
]

end
