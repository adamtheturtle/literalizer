Imports System.Collections.Generic
Module Check
    Function f(a As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim x = 1
        f(x)
    End Sub
End Module
