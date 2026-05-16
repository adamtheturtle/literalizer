Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"project", "alpha"},
        {"lead_task", New Dictionary(Of String, Object) From {{"id", 100}, {"description", "first task"}, {"is_done", False}, {"blocks", New Integer() {102, 103}}}}
    }
End Module
