Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Dictionary(Of String, Object) From {
            {"within_i32", "2024-01-15T12:00:00"},
            {"beyond_i32", "2099-06-15T08:30:00"}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Dictionary(Of String, Object) From {
            {"within_i32", "2024-01-15T12:00:00"},
            {"beyond_i32", "2099-06-15T08:30:00"}
        }
    End Sub
End Module
