Imports System.Collections.Generic
Module Check
    Function f(a As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim ref_data = 1
        f(ref_data)
    End Sub
End Module
