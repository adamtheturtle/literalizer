Imports System.Collections.Generic
Module Check
    Function consume(value As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        consume(-2147483649)
        consume(2147483648)
    End Sub
End Module
