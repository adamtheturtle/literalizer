module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
let my_data : val_t = OList [
    OList [];
    OList [OInt 1; OStr "value"];
    OList [OInt 2; OInt 3]
]

end
