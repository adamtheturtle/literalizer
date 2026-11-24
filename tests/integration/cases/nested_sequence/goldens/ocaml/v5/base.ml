module Check = struct

type val_t =
  | ONull
  | OBool of bool
  | OInt of int
  | OStr of string
  | OList of val_t list
let my_data : val_t = OList [
    OBool true;
    OStr "hi";
    OList [OInt 1; OInt 2];
    ONull
]

end
