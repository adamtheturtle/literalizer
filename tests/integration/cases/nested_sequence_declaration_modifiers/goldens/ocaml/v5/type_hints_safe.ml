module Check = struct

type val_t =
  | ONull
  | OBool of bool
  | OInt of int
  | OStr of string
  | OList of val_t list
let my_data : val_t = OList [
    OList [];
    OList [OInt 1];
    OList [OInt 1; OInt 2];
    OList [OInt 1; OStr "x"; OBool true; ONull];
    OList [OInt 1; OInt 2; OInt 3; OInt 4; OInt 5; OInt 6; OInt 7; OInt 8]
]

end
