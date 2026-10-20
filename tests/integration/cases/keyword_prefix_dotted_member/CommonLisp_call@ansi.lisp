(defun thing (&rest args) (declare (ignore args)) nil)
(defun thing.first_value (&rest args) (declare (ignore args)) nil)
(thing.first_value :value 1)
