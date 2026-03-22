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
  | ODate of (int * int * int)
  | ODatetime of ((int * int * int) * (int * int * int))

let x : val_t = OList [
    OList [OList [OInt 1; OInt 2]; OList [OInt 3; OInt 4]];
    OList [OList [OInt 5]]
]

end
