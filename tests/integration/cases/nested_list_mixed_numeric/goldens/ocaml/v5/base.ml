module Check = struct

type val_t =
  | OInt of int
  | OFloat of float
  | OList of val_t list
let my_data : val_t = OList [
    OList [OInt 1];
    OList [OFloat 2.5]
]

end
