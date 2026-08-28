module [my_data]

record_entry : a, b, c -> {}
record_entry = \_, _, _ -> {}

my_data = record_entry (RStr "a") (RInt 1i128) (RBool Bool.true)
