(defparameter *my_data* (list
    (list (cons "id" 100) (cons "label" "first entry") (cons "enabled" nil) (cons "related_ids" (list 102 103)))
    (list (cons "id" 101) (cons "label" "second entry") (cons "enabled" t) (cons "related_ids" (list 100)))
))
(setf *my_data* (list
    (list (cons "id" 100) (cons "label" "first entry") (cons "enabled" nil) (cons "related_ids" (list 102 103)))
    (list (cons "id" 101) (cons "label" "second entry") (cons "enabled" t) (cons "related_ids" (list 100)))
))
