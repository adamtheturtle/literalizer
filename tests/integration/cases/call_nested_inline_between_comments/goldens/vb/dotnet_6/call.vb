Imports System.Collections.Generic
Module Check
    Function f(a As Object, b As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        f(2, "hello")  ' trailing note
        ' next element
        f(3, "world")
    End Sub
End Module
