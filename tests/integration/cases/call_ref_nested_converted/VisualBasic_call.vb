Imports System.Collections.Generic
Module Check
    Function process(data As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim MyVar = 42
        process(New Object() {MyVar, 42, "static"})
    End Sub
End Module
