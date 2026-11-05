Imports System.Collections.Generic
Module Check
    Function consume(value As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim item = "s"
        consume(item)
    End Sub
End Module
