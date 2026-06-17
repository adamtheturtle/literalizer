(defun put (&rest args) (declare (ignore args)) nil)
(defun get (&rest args) (declare (ignore args)) nil)
(put :key 1 :value 10)
(get :key 1)
