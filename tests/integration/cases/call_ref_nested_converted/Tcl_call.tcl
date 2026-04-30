proc process {args} {}
set my_var 42
process [list [dict create "ref" "myVar"] 42 "static"]
