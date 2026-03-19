Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Dictionary(Of String, Object) From {
            {"date", "2024-01-15"},
            {"datetime", "2024-01-15T12:30:00+00:00"}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Dictionary(Of String, Object) From {
            {"date", "2024-01-15"},
            {"datetime", "2024-01-15T12:30:00+00:00"}
        }
    End Sub
End Module
