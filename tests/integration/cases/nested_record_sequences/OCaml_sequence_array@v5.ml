module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OArray of val_t array
  | OMap of (string * val_t) list
let my_data : val_t array = [|
    OArray [|OMap [("a", OInt 1)]|];
    OArray [|OMap [("a", OInt 2)]|]
|]

end
