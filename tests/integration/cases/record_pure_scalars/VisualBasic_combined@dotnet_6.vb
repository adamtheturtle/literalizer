Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Dictionary(Of String, Object) From {
            {"name", "Alice"},
            {"age", 30},
            {"active", True},
            {"score", 4.5}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Dictionary(Of String, Object) From {
            {"name", "Alice"},
            {"age", 30},
            {"active", True},
            {"score", 4.5}
        }
    End Sub
End Module
