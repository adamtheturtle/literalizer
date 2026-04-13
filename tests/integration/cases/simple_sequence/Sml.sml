structure Check = struct

datatype val_t =
    SNull
  | SBool of bool
  | SInt of int
  | SStr of string
  | SList of val_t list
val my_data : val_t = SList [
    SInt 1,
    SStr "hello",
    SBool true,
    SNull
]

end
