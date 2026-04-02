Module Check
    Sub _declaration()
        Dim my_data = New Dictionary(Of String, Object) From {
            {"1", "one"},
            {"2", "two"},
            {"42", "answer"}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Dictionary(Of String, Object) From {
            {"1", "one"},
            {"2", "two"},
            {"42", "answer"}
        }
    End Sub
End Module
