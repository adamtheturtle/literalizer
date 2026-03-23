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
    OInt 42;
    OFloat 3.14;
    OBool true;
    OBool false;
    OStr "hello \"world\""
]

end
