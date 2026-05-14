Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Object() {
            New Dictionary(Of String, Object) From {{"id", 1}, {"label", "first"}},
            New Dictionary(Of String, Object) From {{"id", 2}, {"label", "second"}},
            New Dictionary(Of String, Object) From {{"id", 3}, {"label", "third"}}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Object() {
            New Dictionary(Of String, Object) From {{"id", 1}, {"label", "first"}},
            New Dictionary(Of String, Object) From {{"id", 2}, {"label", "second"}},
            New Dictionary(Of String, Object) From {{"id", 3}, {"label", "third"}}
        }
    End Sub
End Module
