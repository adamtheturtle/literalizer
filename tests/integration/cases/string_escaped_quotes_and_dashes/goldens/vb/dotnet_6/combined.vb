Module Check
    Sub _declaration()
        Dim my_data = "hello ""world"" -- not a comment"
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = "hello ""world"" -- not a comment"
    End Sub
End Module
