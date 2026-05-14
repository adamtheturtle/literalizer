Imports System.Collections.Generic
Module Check
    Function process(data As Object, count As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim my_var = New Integer() {
            1,
            2,
            3
        }
        Dim my_other = New Integer() {
            4,
            5,
            6
        }
        process(my_var, 42)
        process(my_other, 7)
    End Sub
End Module
