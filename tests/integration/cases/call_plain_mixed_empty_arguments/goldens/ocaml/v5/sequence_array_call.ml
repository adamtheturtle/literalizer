module Check = struct

let make_widget _ = ()
type val_t =
  | OInt of int
  | OStr of string
  | OArray of val_t array
let _ = make_widget([||], [|OInt 1|], [||])
let _ = make_widget([|OStr "text"|], [|OInt 2|], [||])
let _ = make_widget([||], [|OStr "text"|], [||])
let _ = make_widget([|OStr "text"|], [|OInt 2|], [|OInt 3|])

end
