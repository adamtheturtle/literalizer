(defparameter *std* (list
    (cons "nan" #.(sb-int:with-float-traps-masked (:invalid) (- sb-ext:double-float-positive-infinity sb-ext:double-float-positive-infinity)))
    (cons "positive" sb-ext:double-float-positive-infinity)
    (cons "negative" sb-ext:double-float-negative-infinity)
))
