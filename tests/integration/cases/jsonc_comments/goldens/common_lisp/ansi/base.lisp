(defparameter *my_data* (list
    ; A JSONC input case with both comment forms.
    (cons "url" "https://example.org/a/*b*/")  ; detail
    ; continued
    (cons "count" 2)  ; trailing line comment
))
