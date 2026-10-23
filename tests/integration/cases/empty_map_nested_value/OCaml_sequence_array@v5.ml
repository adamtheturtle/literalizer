module Check = struct

type val_t =
  | OStr of string
  | OArray of val_t array
  | OMap of (string * val_t) list
let my_data : val_t array = [|
    OArray [|OMap [("mapping", OMap [])]; OMap []|];
    OArray [|OMap []; OMap [("mapping", OMap [])]|]
|]

end
