module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
  | OSet of val_t list
let my_data : val_t = OList [
    OSet [];
    OSet [OInt 1; OInt 2];
    OList []
]

end
