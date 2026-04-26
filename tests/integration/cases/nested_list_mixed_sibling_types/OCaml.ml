module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
let my_data : val_t = OList [
    OList [OInt 1; OInt 2];
    OList [];
    OList [OStr "a"; OStr "b"]
]

end
