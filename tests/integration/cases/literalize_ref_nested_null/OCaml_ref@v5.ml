module Check = struct

type val_t =
  | ONull
  | OList of val_t list
let my_null : val_t = ONull
let my_data : val_t = OList [
    my_null;
    ONull
]

end
