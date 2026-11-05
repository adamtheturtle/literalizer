Imports System.Collections.Generic
Module Check
    Function consume(value As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        consume(1)
    End Sub
End Module
