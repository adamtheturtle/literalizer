module Check = struct

type val_t =
  | OBool of bool
  | OInt of int
  | OStr of string
  | OSet of val_t list
let my_data : val_t = OSet [
    OBool true;
    OInt 42;
    OStr "apple"
]

end
