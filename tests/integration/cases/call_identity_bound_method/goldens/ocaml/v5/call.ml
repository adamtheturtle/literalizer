module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
module Thing = struct
let go _ = ()
end
let item : val_t = OList [
    OInt 1;
    OInt 2
]
let _ = Thing.go(item)

end
