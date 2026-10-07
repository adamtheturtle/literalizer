Module Check
    Sub _declaration()
        Dim my_data = New HashSet(Of Double) From {
            2.5,
            1
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New HashSet(Of Double) From {
            2.5,
            1
        }
    End Sub
End Module
