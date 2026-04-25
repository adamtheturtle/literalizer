module Check = struct

type val_t =
  | ODate of (int * int * int)
  | OList of val_t list
let my_data : val_t = OList [
    OList [ODate (2026, 1, 1); ODate (2026, 1, 2)];
    OList [];
    OList [ODate (2026, 2, 3); ODate (2026, 2, 4)]
]

end
