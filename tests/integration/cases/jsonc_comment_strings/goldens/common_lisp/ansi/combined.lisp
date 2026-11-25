(defparameter *my_data* (list
    ; strings stay data
    "https://example.org/a/*b*/"  ; URL annotation
    "escaped quote: \" // still data"
    "backslash: \\"  ; outside the string
    "/* not a comment */"
))
(setf *my_data* (list
    ; strings stay data
    "https://example.org/a/*b*/"  ; URL annotation
    "escaped quote: \" // still data"
    "backslash: \\"  ; outside the string
    "/* not a comment */"
))
