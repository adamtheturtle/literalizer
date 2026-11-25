module Check = struct

module Thing = struct
let go _ = ()
end
type val_t =
  | OInt of int
  | OStr of string
  | OArray of val_t array
let _ = Thing.go([||], [|OInt 1|], [||])
let _ = Thing.go([|OStr "text"|], [|OInt 2|], [||])
let _ = Thing.go([||], [|OStr "text"|], [||])
let _ = Thing.go([|OStr "text"|], [|OInt 2|], [|OInt 3|])

end
