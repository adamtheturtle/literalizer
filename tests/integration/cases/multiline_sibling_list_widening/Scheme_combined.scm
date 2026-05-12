(define my_data (list
    "omap_value" (list "first" 1)
    "sibling_lists" (list "numbers" (list 1 2) "strings" (list "x" "y"))
    "ref_marker_present" (list "$keep" "z")
))
(set! my_data (list
    "omap_value" (list "first" 1)
    "sibling_lists" (list "numbers" (list 1 2) "strings" (list "x" "y"))
    "ref_marker_present" (list "$keep" "z")
))
