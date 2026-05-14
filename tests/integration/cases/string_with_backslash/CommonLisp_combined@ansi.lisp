(defparameter *my_data* (list
    "C:\\path\\to\\file"
    "back\\\\slash"
    "hello \\\"world\\\""
    "path\\to \"# file"
    "trailing\\"
    "both \"quotes''' here"
    "line1\\nline2
with newline"
))
(setf *my_data* (list
    "C:\\path\\to\\file"
    "back\\\\slash"
    "hello \\\"world\\\""
    "path\\to \"# file"
    "trailing\\"
    "both \"quotes''' here"
    "line1\\nline2
with newline"
))
