module Check = struct

type val_t =
  | OBool of bool
  | OInt of int
  | OFloat of float
  | OStr of string
  | OList of val_t list
let my_data : val_t = OList [
    OInt 42;
    OFloat 3.14;
    OBool true;
    OBool false;
    OStr "hello \"world\""
]

end
