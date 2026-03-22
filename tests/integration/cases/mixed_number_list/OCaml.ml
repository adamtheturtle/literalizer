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

let x : val_t = OList [
    OInt 1;
    OFloat 2.5;
    OInt 3
]

end
