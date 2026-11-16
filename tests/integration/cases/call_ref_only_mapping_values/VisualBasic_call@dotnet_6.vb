Imports System.Collections.Generic
Module Check
    Function consume(value As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim item = 42
        consume(New Dictionary(Of String, Object) From {{"field", item}})
    End Sub
End Module
