module Check = struct

type val_t =
  | OFloat of float
  | OList of val_t list
let my_data : val_t = OList [
    OList [OFloat 1.500000; OFloat 2.500000];
    OList [OFloat 3.500000; OFloat 4.500000]
]

end
