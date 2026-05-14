module Check = struct

type val_t =
  | OBool of bool
  | OInt of int
  | OStr of string
  | OList of val_t list
let my_data : val_t = OList [
    OInt 1;
    OStr "hello";
    OBool true
]

end
