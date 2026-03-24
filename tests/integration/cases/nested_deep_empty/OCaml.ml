module Check = struct

type val_t =
  | OList of val_t list
let my_data : val_t = OList [
    OList [OList []; OList []]
]

end
