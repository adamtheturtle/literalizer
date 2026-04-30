proc process {args} {}
set my_var 42
process [dict create "key" [dict create "ref" "my_var"] "count" 42]
