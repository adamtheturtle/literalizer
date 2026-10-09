module Check = struct

type val_t =
  | ONull
  | OInt of int
  | OList of val_t list
let my_value : val_t = OList [
    OInt 1;
    OInt 2
]
let my_data : val_t = my_value

end
