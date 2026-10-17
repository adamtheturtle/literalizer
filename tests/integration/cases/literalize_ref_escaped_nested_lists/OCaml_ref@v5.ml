module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let existing : val_t = OInt 1
let my_data : val_t = OList [
    OInt 0;
    OList [OList [existing]]
]

end
