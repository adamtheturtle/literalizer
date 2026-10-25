module Check = struct

type val_t =
  | OInt of int
  | ODatetime of ((int * int * int) * (int * int * int))
  | OList of val_t list
let my_data : val_t = OList [
    ODatetime ((2000, 1, 1), (1, 2, 3));
    OInt 1
]

end
