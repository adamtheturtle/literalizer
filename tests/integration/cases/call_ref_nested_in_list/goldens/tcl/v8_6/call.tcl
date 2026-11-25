proc process {args} {}
set my_var 42
set my_other 7
process [list my_var 42 "static"]
process [list my_other 7 "label"]
