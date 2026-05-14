module Check = struct

type val_t =
  | OSet of val_t list
let my_data : val_t = OSet []

end
