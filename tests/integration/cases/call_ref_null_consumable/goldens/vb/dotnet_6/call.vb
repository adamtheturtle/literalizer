Imports System.Collections.Generic
Module Check
    Function consume(value As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim my_null = Nothing
        Dim regular_null = Nothing
        consume(my_null)
        consume(regular_null)
    End Sub
End Module
