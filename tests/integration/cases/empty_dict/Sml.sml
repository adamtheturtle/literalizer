structure Check = struct

datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap []

end
