module Check = struct

type val_t =
  | OStr of string
  | OSet of val_t list
let my_data : val_t = OSet [
    OStr "1901-12-13T20:45:51";
    OStr "1901-12-13T20:45:52";
    OStr "2038-01-19T03:14:07";
    OStr "2038-01-19T03:14:08"
]

end
