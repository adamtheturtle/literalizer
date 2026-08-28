Imports System.Collections.Generic
Module Check
    Function f(a As Object, b As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        f(2, "hello")  ' trailing note
        f(3, "world")  ' another note
    End Sub
End Module
