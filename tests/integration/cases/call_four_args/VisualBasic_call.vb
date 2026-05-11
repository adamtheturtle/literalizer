Imports System.Collections.Generic
Module Check
    Function process(a As Object, b As Object, c As Object, d As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        process(1, 2, 3, 4)
        process(10, 20, 30, 40)
    End Sub
End Module
