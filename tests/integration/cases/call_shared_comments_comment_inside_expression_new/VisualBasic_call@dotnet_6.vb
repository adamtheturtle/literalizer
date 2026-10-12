Module Check
    Function make_widget(count As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim my_data = make_widget(42) // inner
         + 1
    End Sub
End Module
