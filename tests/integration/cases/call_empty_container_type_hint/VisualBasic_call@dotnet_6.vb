Imports System.Collections.Generic
Module Check
    Function process(values As Object, count As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        process(New Object() {1, New Dictionary(Of String, Object) From {}}, 42)
    End Sub
End Module
