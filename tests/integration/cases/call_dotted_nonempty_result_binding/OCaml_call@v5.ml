module Check = struct

module Thing = struct
let go _ = ()
end
type val_t =
  | OInt of int
  | OList of val_t list
let my_data = Thing.go(OList [OInt 1])

end
