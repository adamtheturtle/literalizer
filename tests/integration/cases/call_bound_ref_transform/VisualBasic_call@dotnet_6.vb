Imports System.Collections.Generic
Module Check
    Function f(a As Object) As Object
        Return Nothing
    End Function
    Function repr(_arg As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim ref_data = 1
        repr(f(ref_data))
    End Sub
End Module
