Module Check
    Sub _declaration()
        Dim my_data = New HashSet(Of String) From {
            "apple",
            "banana",
            "cherry"
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New HashSet(Of String) From {
            "apple",
            "banana",
            "cherry"
        }
    End Sub
End Module
