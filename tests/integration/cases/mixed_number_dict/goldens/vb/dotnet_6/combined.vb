Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Dictionary(Of String, Object) From {
            {"a", 1},
            {"b", 2.5},
            {"c", 3}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Dictionary(Of String, Object) From {
            {"a", 1},
            {"b", 2.5},
            {"c", 3}
        }
    End Sub
End Module
