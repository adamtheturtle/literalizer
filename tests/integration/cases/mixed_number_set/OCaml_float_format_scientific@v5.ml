module Check = struct

type val_t =
  | OInt of int
  | OFloat of float
  | OSet of val_t list
let my_data : val_t = OSet [
    OFloat 2.5;
    OInt 1
]

end
