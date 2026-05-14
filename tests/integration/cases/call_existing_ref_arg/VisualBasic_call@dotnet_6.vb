Imports System.Collections.Generic
Module Check
    Function process(value As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim existing = 42
        process(existing)
    End Sub
End Module
