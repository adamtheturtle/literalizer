module Check = struct

type val_t =
  | OStr of string
  | OSet of val_t list
let my_data : val_t = OSet [
    OStr "2099-06-15T08:30:00"
]

end
