Module Check
    Function consume(value As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim value = Nothing
        consume(value)
    End Sub
End Module
