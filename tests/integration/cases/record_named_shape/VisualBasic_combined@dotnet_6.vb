Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Object() {
            New Dictionary(Of String, Object) From {{"id", 100}, {"label", "first item"}, {"enabled", False}, {"related_ids", New Integer() {102, 103}}},
            New Dictionary(Of String, Object) From {{"id", 101}, {"label", "second item"}, {"enabled", True}, {"related_ids", New Integer() {100}}}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Object() {
            New Dictionary(Of String, Object) From {{"id", 100}, {"label", "first item"}, {"enabled", False}, {"related_ids", New Integer() {102, 103}}},
            New Dictionary(Of String, Object) From {{"id", 101}, {"label", "second item"}, {"enabled", True}, {"related_ids", New Integer() {100}}}
        }
    End Sub
End Module
