module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let my_data : val_t = OList [
    OInt 0o67405553164730777777;
    OInt (-0o67405553164730777777)
]

end
