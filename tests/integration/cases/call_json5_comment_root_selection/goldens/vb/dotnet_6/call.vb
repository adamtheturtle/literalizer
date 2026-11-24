Imports System.Collections.Generic
Module Check
    Function f(a As Object, b As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        ' selected heading
        f(1, 2)  ' selected inline
    End Sub
End Module
