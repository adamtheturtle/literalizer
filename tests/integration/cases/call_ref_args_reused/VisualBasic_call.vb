Imports System.Collections.Generic
Module Check
    Function process(data As Object, count As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim shared = 1
        Dim other = 2
        process(shared, 1)
        process(other, 0)
        process(shared, 8)
    End Sub
End Module
