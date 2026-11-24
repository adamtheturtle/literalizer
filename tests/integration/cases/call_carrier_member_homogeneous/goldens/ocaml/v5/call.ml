module Check = struct

module App = struct
let go _ = ()
end
type val_t =
  | OInt of int
  | OList of val_t list
let _ = App.go(OList [OInt 1], OList [OInt 2])

end
