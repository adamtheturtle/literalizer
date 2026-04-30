Imports System.Collections.Generic
Module Check
    Function process(data As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim my_var = 42
        process(New Dictionary(Of String, Object) From {{"key", New Dictionary(Of String, Object) From {{"ref", "my_var"}}}, {"count", 42}})
    End Sub
End Module
