(defparameter *my_data* (list
    (cons "key
with
newlines" "value1")
    (cons "key	with	tabs" "value2")
    (cons "" "value3")
))
(setf *my_data* (list
    (cons "key
with
newlines" "value1")
    (cons "key	with	tabs" "value2")
    (cons "" "value3")
))
