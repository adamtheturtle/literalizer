module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let ref_x : val_t = OInt 3
let my_data : val_t = OList [
    ref_x;
    OInt 1;
    OInt 2
]

end
