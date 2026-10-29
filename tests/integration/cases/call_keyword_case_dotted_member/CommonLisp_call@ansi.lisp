(defun thing (&rest args) (declare (ignore args)) nil)
(defun thing.Before (&rest args) (declare (ignore args)) nil)
(thing.Before :value 1)
