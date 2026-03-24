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

[|
    OInt 1;
    OStr "hello";
    OBool true;
    ONull
|]

end
