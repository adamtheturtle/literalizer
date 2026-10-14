Module Check
    Function make_widget(count As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim my_data = make_widget(42)
        my_data = make_widget(my_data)
        // note
        make_widget(my_data)
    End Sub
End Module
