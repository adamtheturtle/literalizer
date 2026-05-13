module Check = struct

type val_t =
  | OInt of int
  | OSet of val_t list
let my_data : val_t = OSet [
    OInt 1;
    OInt 1099511627776
]

end
