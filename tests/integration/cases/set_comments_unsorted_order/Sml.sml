structure Check = struct

datatype val_t =
    SStr of string
  | SSet of val_t list
val my_data : val_t = SSet [
    (* before apple *)
    SStr "apple",
    SStr "banana"  (* banana inline *)
    (* trailing *)
]

end
