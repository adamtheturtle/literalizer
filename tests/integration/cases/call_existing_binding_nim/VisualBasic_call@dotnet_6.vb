Module Check
    Function make_widget(count As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim my_data = make_widget(0)
        my_data = make_widget(1)
        make_widget(my_data)
    End Sub
End Module
