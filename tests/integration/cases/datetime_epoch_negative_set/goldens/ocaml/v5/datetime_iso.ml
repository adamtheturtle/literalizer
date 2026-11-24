module Check = struct

type val_t =
  | OStr of string
  | OSet of val_t list
let my_data : val_t = OSet [
    OStr "1969-12-31T23:59:59+00:00"
]

end
