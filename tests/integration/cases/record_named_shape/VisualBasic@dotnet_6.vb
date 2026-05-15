Imports System.Collections.Generic
Module Check
    Dim my_data = New Object() {
        New Dictionary(Of String, Object) From {{"id", 100}, {"description", "first task"}, {"is_done", False}, {"blocks", New Integer() {102, 103}}},
        New Dictionary(Of String, Object) From {{"id", 101}, {"description", "second task"}, {"is_done", True}, {"blocks", New Object() {}}}
    }
End Module
