(defparameter *my_data* (list
    (list (cons "id" 100) (cons "description" "first task") (cons "is_done" nil) (cons "blocks" (list 102 103)))
    (list (cons "id" 101) (cons "description" "second task") (cons "is_done" t) (cons "blocks" nil))
))
(setf *my_data* (list
    (list (cons "id" 100) (cons "description" "first task") (cons "is_done" nil) (cons "blocks" (list 102 103)))
    (list (cons "id" 101) (cons "description" "second task") (cons "is_done" t) (cons "blocks" nil))
))
