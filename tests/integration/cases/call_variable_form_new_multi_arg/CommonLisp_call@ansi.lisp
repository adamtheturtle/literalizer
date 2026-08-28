(defun record_entry (&rest args) (declare (ignore args)) 0)
(defparameter *my_data* (record_entry :s "a" :n 1 :b t))
