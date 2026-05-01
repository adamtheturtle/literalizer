Imports System.Collections.Generic
Module Check
    Function send(value As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        send(New Dictionary(Of String, Object) From {{"a", 1}, {"b", "x"}})
    End Sub
End Module
