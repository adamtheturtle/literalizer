module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let my_data : val_t = OList [
    OInt 1;
    OInt 1_099_511_627_776
]

end
