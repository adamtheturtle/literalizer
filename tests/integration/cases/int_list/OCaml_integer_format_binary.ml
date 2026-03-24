module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let my_data : val_t = OList [
    OInt 0b1;
    OInt 0b10;
    OInt 0b11
]

end
