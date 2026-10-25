Imports System.Collections.Generic
Module Check
    Function f(a As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        f(New Integer() {1})  ' note
    End Sub
End Module
