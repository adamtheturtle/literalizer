Module Check
    Function make_widget(count As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim my_data = ($"{(true ? "// payload" : "ok")}").Length >= 0 ? make_widget(42) : make_widget(42)
    End Sub
End Module
