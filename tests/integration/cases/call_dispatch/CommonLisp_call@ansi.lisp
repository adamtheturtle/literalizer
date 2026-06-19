(defun store_item (&rest args) (declare (ignore args)) nil)
(defun read_item (&rest args) (declare (ignore args)) nil)
(store_item :key 1 :value 10)
(read_item :key 1)
