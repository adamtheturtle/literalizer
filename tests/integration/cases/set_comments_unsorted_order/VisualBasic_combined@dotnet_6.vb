Module Check
    Sub _declaration()
        ' before apple
        ' banana inline
        ' trailing
        Dim my_data = New HashSet(Of String) From {
            "apple",
            "banana"
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        ' before apple
        ' banana inline
        ' trailing
        my_data = New HashSet(Of String) From {
            "apple",
            "banana"
        }
    End Sub
End Module
