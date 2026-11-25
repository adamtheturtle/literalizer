module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let my_data : val_t = OList [
    OInt 999999999999999999;
    OInt (-999999999999999999)
]

end
