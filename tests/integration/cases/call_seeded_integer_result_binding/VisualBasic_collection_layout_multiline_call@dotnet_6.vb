Module Check
    Function make_widget(count As Object) As Object
        Return Nothing
    End Function
    Function consume(count As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim my_data = make_widget(42)
        consume(my_data)
        my_data = make_widget(42)
        consume(my_data)
    End Sub
End Module
