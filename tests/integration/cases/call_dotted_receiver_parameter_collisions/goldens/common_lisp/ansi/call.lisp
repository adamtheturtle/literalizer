(defun api (&rest args) (declare (ignore args)) nil)
(defun api.worker (&rest args) (declare (ignore args)) nil)
(defun api.worker.process (&rest args) (declare (ignore args)) nil)
(api.worker.process :self nil :self_ nil)
