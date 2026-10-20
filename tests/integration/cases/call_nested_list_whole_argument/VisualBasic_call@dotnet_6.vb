Imports System.Collections.Generic
Module Check
    Function f(a As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        f(New Integer()() {New Integer() {1, 2}, New Integer() {3}})
    End Sub
End Module
