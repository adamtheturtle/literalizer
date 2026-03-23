Module Check
    Sub _declaration()
        Dim my_data = New HashSet(Of Object) From {
            True,
            42,
            "apple"
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New HashSet(Of Object) From {
            True,
            42,
            "apple"
        }
    End Sub
End Module
