Imports System.Collections.Generic
Module Check
    Function process(data As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim unknown_value = New Object() {}
        process(New Object() {unknown_value})
    End Sub
End Module
