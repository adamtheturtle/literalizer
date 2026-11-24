Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Dictionary(Of String, Object) From {
            {"name", "Alice"},
            {"age", 30},
            {"active", True},
            {"score", Nothing},
            {"joined", New DateOnly(2024, 1, 15)},
            {"last_login", "2024-01-15T12:30:00+00:00"},
            {"avatar", "48656c6c6f"}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Dictionary(Of String, Object) From {
            {"name", "Alice"},
            {"age", 30},
            {"active", True},
            {"score", Nothing},
            {"joined", New DateOnly(2024, 1, 15)},
            {"last_login", "2024-01-15T12:30:00+00:00"},
            {"avatar", "48656c6c6f"}
        }
    End Sub
End Module
