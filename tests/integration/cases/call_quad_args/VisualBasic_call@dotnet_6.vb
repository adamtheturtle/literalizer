Imports System.Collections.Generic
Module Check
    Function process(a As Object, b As Object, c As Object, d As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        process(1, 2, 3, 4)
        process(5, 6, 7, 8)
    End Sub
End Module
