datatype val_t =
    SReal of real
  | SList of val_t list
val my_data : val_t = SList [
    SReal 5.0E~324,
    SReal 2.2250738585072014E~308,
    SReal 1.0E~307,
    SReal 1.0E21,
    SReal (~1.5E300),
    SReal 1.7976931348623157E308,
    SReal (~1.7976931348623157E308)
]
val _ = my_data
