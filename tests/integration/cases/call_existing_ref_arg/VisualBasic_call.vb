Imports System.Collections.Generic
Module Check
    Function send(value As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim existing = 42
        send(existing)
    End Sub
End Module
