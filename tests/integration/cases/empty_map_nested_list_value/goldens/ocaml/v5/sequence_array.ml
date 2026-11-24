module Check = struct

type val_t =
  | OStr of string
  | OArray of val_t array
  | OMap of (string * val_t) list
let my_data : val_t array = [|
    OArray [|OMap [("values", OArray [|OArray [||]|])]; OMap []|];
    OArray [|OMap []; OMap [("values", OArray [|OArray [||]|])]|]
|]

end
