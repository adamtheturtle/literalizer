module Check = struct

module Thing = struct
let go _ = ()
end
type val_t =
  | OList of val_t list
let _ = Thing.go()

end
