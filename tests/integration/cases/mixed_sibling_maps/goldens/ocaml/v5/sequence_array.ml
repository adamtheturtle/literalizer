module Check = struct

type val_t =
  | ONull
  | OInt of int
  | OStr of string
  | OArray of val_t array
  | OMap of (string * val_t) list
let my_data : val_t array = [|
    OArray [|OMap [("a", OInt 1)]; OMap [("a", ONull)]; OInt 42|];
    OArray [|OMap [("a", OInt 1)]; OMap [("a", OStr "s")]; OInt 42|];
    OArray [|OMap [("a", OInt 1)]; OMap [("a", ONull)]|];
    OArray [|OMap [("a", OInt 1)]; OMap [("a", OStr "s")]|]
|]

end
