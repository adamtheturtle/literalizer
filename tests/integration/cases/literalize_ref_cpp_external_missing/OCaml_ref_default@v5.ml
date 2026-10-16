module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let item : val_t = OList [
    OInt 1;
    OInt 2
]
let my_data : val_t = OList [
    OInt 1;
    OInt 2
]
(void)my_data;
let my_data : val_t = item
(void)my_data;

end
