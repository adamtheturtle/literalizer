Module Check
    Function make_widget(count As Object) As Object
        Return Nothing
    End Function
    Function consume_widget(count As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim my_data = make_widget(0)
        consume_widget(my_data)
        my_data = make_widget(1)
        consume_widget(my_data)
    End Sub
End Module
