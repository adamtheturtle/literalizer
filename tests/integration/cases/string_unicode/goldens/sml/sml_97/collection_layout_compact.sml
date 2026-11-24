datatype val_t =
    SStr of string
  | SList of val_t list
val my_data : val_t = SList [
    SStr "caf\195\169",
    SStr "\228\184\173\230\150\135",
    SStr "\240\159\152\128"
]
val _ = my_data
