module Check = struct

let make_widget _ = ()
type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
let _ = make_widget(OList [], OList [OInt 1], OList [])
let _ = make_widget(OList [OStr "text"], OList [OInt 2], OList [])
let _ = make_widget(OList [], OList [OStr "text"], OList [])
let _ = make_widget(OList [OStr "text"], OList [OInt 2], OList [OInt 3])

end
