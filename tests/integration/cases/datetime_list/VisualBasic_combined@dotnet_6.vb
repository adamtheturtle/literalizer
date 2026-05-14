Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New String() {
            "2024-01-15T12:30:00.123456+00:00",
            "2024-06-01T08:00:00+00:00"
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New String() {
            "2024-01-15T12:30:00.123456+00:00",
            "2024-06-01T08:00:00+00:00"
        }
    End Sub
End Module
