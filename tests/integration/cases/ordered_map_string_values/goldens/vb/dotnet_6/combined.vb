Module Check
    Sub _declaration()
        Dim my_data = New Dictionary(Of String, Object) From {
            {"first", "one"},
            {"second", "two"},
            {"third", "three"}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Dictionary(Of String, Object) From {
            {"first", "one"},
            {"second", "two"},
            {"third", "three"}
        }
    End Sub
End Module
