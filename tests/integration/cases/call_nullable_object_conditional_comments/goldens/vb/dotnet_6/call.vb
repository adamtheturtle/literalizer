Module Check
    Function make_widget(count As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim my_data = If(make_widget(42) IsNot Nothing,
        make_widget(42),  ' inner
        Nothing) ' trailing
    End Sub
End Module
