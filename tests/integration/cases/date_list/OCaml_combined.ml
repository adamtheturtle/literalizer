module Check = struct

type val_t =
  | ODate of (int * int * int)
  | OList of val_t list
let my_data : val_t = OList [
    ODate (2024, 1, 15);
    ODate (2024, 2, 20)
]

end
