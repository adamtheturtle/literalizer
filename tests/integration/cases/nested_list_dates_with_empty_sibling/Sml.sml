structure Check = struct

datatype val_t =
    SDate of (int * int * int)
  | SList of val_t list
val my_data : val_t = SList [
    SList [SDate (2026, 1, 1), SDate (2026, 1, 2)],
    SList [],
    SList [SDate (2026, 2, 3), SDate (2026, 2, 4)]
]

end
