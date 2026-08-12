Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Dictionary(Of String, Object) From {
            {"a", New Dictionary(Of String, Object) From {{"b", 1}}},
            {"list", New Integer() {1, 2}}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Dictionary(Of String, Object) From {
            {"a", New Dictionary(Of String, Object) From {{"b", 1}}},
            {"list", New Integer() {1, 2}}
        }
    End Sub
End Module
