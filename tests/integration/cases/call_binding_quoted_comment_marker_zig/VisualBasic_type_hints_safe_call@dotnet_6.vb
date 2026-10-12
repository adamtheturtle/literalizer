Module Check
    Function make_widget(text As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim my_data = make_widget("first ""quote""" & Chr(10) & "// string body") // note
        // extra
    End Sub
End Module
