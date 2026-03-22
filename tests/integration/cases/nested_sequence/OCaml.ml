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
    OBool true;
    OStr "hi";
    OList [OInt 1; OInt 2];
    ONull
]

end
