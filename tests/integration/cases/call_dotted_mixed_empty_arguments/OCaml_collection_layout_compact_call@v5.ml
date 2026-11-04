module Check = struct

module Thing = struct
let go _ = ()
end
type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
let _ = Thing.go(OList [], OList [OInt 1], OList [])
let _ = Thing.go(OList [OStr "text"], OList [OInt 2], OList [])
let _ = Thing.go(OList [], OList [OStr "text"], OList [])
let _ = Thing.go(OList [OStr "text"], OList [OInt 2], OList [OInt 3])

end
