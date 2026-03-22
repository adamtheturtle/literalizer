Module Check
    Sub _declaration()
        Dim my_data = New Dictionary(Of String, Object) From {
            {"name", "Alice"},
            {"age", 30},
            {"active", True}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Dictionary(Of String, Object) From {
            {"name", "Alice"},
            {"age", 30},
            {"active", True}
        }
    End Sub
End Module
