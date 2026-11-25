Module Check
    Function consume_widget(arg_value As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        consume_widget(New HashSet(Of Integer) From {
            1,
            2
        })
    End Sub
End Module
