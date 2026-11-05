Imports System.Collections.Generic
Module Check
    Function consume(value As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim external_value = 1
        consume(external_value)
    End Sub
End Module
