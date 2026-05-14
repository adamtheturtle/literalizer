module Check = struct

type val_t =
  | OStr of string
  | OSet of val_t list
let my_data : val_t = OSet [
    OStr "apple";
    OStr "banana";
    OStr "cherry"
]

end
