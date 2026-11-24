proc f {args} {}
f [list [list "DEL" "b" "10"] [list "ADD" "a" "x"]]  ;# note
;# next call
f [list [list "ADD" "c" "y"]]
