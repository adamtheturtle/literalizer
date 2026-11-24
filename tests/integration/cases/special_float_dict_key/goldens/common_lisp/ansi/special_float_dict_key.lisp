(defparameter *my_data* (list
    (cons #.(sb-int:with-float-traps-masked (:invalid) (- sb-ext:double-float-positive-infinity sb-ext:double-float-positive-infinity)) 1)
))
