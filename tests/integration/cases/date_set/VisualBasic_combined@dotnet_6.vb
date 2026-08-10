Module Check
    Sub _declaration()
        Dim my_data = New HashSet(Of String) From {
            New DateOnly(2024, 1, 15),
            New DateOnly(2024, 6, 1)
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New HashSet(Of String) From {
            New DateOnly(2024, 1, 15),
            New DateOnly(2024, 6, 1)
        }
    End Sub
End Module
