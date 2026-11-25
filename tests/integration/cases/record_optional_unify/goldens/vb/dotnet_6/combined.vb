Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Dictionary(Of String, Object) From {
            {"items", New Object() {New Dictionary(Of String, Object) From {{"id", 1}}, New Dictionary(Of String, Object) From {{"id", 2}, {"count", 10}}, New Dictionary(Of String, Object) From {{"id", 3}, {"count", 20}}}}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Dictionary(Of String, Object) From {
            {"items", New Object() {New Dictionary(Of String, Object) From {{"id", 1}}, New Dictionary(Of String, Object) From {{"id", 2}, {"count", 10}}, New Dictionary(Of String, Object) From {{"id", 3}, {"count", 20}}}}
        }
    End Sub
End Module
