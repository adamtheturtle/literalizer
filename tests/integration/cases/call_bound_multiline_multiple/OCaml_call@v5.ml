module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let f _ = ()
let ref_data : val_t = OList [
    OInt 1;
    OInt 2
]
let _ = f(OList [
    ref_data
])
let _ = f(OList [
    ref_data
])

end
