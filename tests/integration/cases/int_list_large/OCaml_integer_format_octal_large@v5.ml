module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let my_data : val_t = OList [
    OInt 0o3641100;
    OInt (-0o2322);
    OInt 0o377;
    OInt (-0o12)
]

end
