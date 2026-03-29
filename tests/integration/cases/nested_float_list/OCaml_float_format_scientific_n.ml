module Check = struct

type val_t =
  | OFloat of float
  | OList of val_t list
let my_data : val_t = OList [
    OList [OFloat 1.5; OFloat 2.5];
    OList [OFloat 3.5; OFloat 4.5]
]

end
