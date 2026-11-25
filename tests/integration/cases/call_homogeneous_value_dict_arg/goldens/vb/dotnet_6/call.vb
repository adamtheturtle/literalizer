Imports System.Collections.Generic
Module Check
    Function process(value As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        process(New Dictionary(Of String, Object) From {{"a", 1}, {"b", 2}})
    End Sub
End Module
