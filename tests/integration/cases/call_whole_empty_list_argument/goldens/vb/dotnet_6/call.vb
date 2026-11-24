Imports System.Collections.Generic
Module Check
    Function f(a As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        f(New Object() {})
    End Sub
End Module
