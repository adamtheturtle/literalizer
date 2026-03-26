Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Object() {
            New Dictionary(Of String, Object) From {{"x", 1}, {"y", 2.5}},
            New Dictionary(Of String, Object) From {{"x", 3}, {"y", 4.0}}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Object() {
            New Dictionary(Of String, Object) From {{"x", 1}, {"y", 2.5}},
            New Dictionary(Of String, Object) From {{"x", 3}, {"y", 4.0}}
        }
    End Sub
End Module
