proc process {args} {}
set my_var 42
set my_other 7
process [list [dict create "ref" "my_var"] 42 "static"]
process [list [dict create "ref" "my_other"] 7 "label"]
