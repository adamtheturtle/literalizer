Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Dictionary(Of String, Object) From {
            {"a", 1},
            {"b", 3000000000},
            {"c", "x"}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Dictionary(Of String, Object) From {
            {"a", 1},
            {"b", 3000000000},
            {"c", "x"}
        }
    End Sub
End Module
