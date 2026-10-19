module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let my_data : val_t = OList [
    OList [OInt 1; OList []];
    OList [OInt 2; OList [OInt 3]]
]

end
