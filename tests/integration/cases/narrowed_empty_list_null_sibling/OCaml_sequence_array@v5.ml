module Check = struct

type val_t =
  | ONull
  | OArray of val_t array
let my_data : val_t array = [|
    OArray [|ONull|];
    OArray [||]
|]

end
