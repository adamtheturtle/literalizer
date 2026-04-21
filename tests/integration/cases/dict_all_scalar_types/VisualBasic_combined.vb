Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Dictionary(Of String, Object) From {
            {"s", "string"},
            {"i", 1},
            {"f", 1.5},
            {"b", True},
            {"n", Nothing},
            {"d", "2024-01-15"},
            {"dt", "2024-01-15T12:00:00"},
            {"by", "48656c6c6f"}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Dictionary(Of String, Object) From {
            {"s", "string"},
            {"i", 1},
            {"f", 1.5},
            {"b", True},
            {"n", Nothing},
            {"d", "2024-01-15"},
            {"dt", "2024-01-15T12:00:00"},
            {"by", "48656c6c6f"}
        }
    End Sub
End Module
