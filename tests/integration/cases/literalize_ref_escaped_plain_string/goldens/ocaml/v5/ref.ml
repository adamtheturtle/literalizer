module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
let my_data : val_t = OList [
    OInt 0;
    OList [OList [OStr "plain"]]
]

end
