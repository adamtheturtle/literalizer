Imports System.Collections.Generic
Module Check
    Function f(_ As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        f(1)
    End Sub
End Module
