Module Check
    Sub _declaration()
        ' inline comment
        ' before banana
        ' trailing
        Dim my_data = New HashSet(Of String) From {
            "apple",
            "banana"
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        ' inline comment
        ' before banana
        ' trailing
        my_data = New HashSet(Of String) From {
            "apple",
            "banana"
        }
    End Sub
End Module
