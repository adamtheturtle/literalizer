set my_data [list \
    [dict create "input" [dict create "name" "alice" "city" "paris"] "expected" [dict create "count" 1 "total" 2]] \
    [dict create "input" [dict create "name" 10 "city" 20] "expected" [dict create "count" "done" "total" "pending"]] \
]
