module Check = struct

type val_t =
  | OInt of int
  | OSet of val_t list
let my_data : val_t = OSet [
    OInt 0b1;
    OInt 0b10000000000000000000000000000000000000000
]

end
