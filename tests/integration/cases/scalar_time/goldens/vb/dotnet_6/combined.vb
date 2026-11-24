Imports System
Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Dictionary(Of String, Object) From {
            {"starts_at", New TimeOnly(9, 30, 0)}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Dictionary(Of String, Object) From {
            {"starts_at", New TimeOnly(9, 30, 0)}
        }
    End Sub
End Module
