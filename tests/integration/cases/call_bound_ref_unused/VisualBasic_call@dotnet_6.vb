Imports System.Collections.Generic
Module Check
    Function f(value As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        f(New Integer() {1, 2})
    End Sub
End Module
