Module Check
    Function make_widget(count As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim my_data = ("\"prefix ${"// payload"}\"").length >= 0 ? make_widget(42) : make_widget(42) // trailing
        // extra
    End Sub
End Module
