Module Check
    Function make_widget(count As Object) As Object
        Return Nothing
    End Function
    Function consume(count As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim my_data = make_widget(7)
        consume(my_data)
        my_data = If(make_widget(13) IsNot Nothing,
        make_widget(13),  ' inner
        Nothing) ' trailing
        consume(my_data)
    End Sub
End Module
