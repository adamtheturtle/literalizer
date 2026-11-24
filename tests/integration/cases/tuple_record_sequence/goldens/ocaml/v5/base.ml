module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OList [
    OMap [("call", OStr "send"); ("args", OList [OInt 1; OStr "email"; OStr "a@gmail.com"; OInt 100])];
    OMap [("call", OStr "recv"); ("args", OList [OInt 2; OStr "sms"; OStr "b@example.com"; OInt 200])]
]

end
