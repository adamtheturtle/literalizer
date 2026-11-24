Module Check
    Sub _declaration()
        Dim my_data = New HashSet(Of Integer) From {
            1,
            2,
            3
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New HashSet(Of Integer) From {
            1,
            2,
            3
        }
    End Sub
End Module
