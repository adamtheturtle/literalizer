(defparameter *my_data* (list
    sb-ext:double-float-positive-infinity
    sb-ext:double-float-negative-infinity
    #.(sb-int:with-float-traps-masked (:invalid) (- sb-ext:double-float-positive-infinity sb-ext:double-float-positive-infinity))
))
