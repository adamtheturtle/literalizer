Module Check
    Sub _declaration()
        Dim my_data = New HashSet(Of String) From {
            "2024-01-15",
            "2024-06-01"
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New HashSet(Of String) From {
            "2024-01-15",
            "2024-06-01"
        }
    End Sub
End Module
