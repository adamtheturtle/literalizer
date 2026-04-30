Imports System.Collections.Generic
Module Check
    Function process(data As Object, count As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim single_var = New Integer() {
            4,
            5,
            6
        }
        Dim repeated_var = 1
        process(repeated_var, 1)
        process(single_var, 0)
        process(repeated_var, 8)
    End Sub
End Module
