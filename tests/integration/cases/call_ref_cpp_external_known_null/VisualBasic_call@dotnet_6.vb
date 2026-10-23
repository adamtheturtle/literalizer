Module Check
    Function consume(value As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim item = Nothing
        consume(item)
    End Sub
End Module
