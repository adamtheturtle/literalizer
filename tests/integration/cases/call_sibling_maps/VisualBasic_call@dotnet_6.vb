Imports System.Collections.Generic
Module Check
    Function process(value As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        process(New Dictionary(Of String, Object) From {{"value", 1}})
        process(New Dictionary(Of String, Object) From {{"value", "hello"}})
    End Sub
End Module
