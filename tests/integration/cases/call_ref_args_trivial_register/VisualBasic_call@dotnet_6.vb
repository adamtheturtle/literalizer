Imports System.Collections.Generic
Module Check
    Function process(value As Object, count As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim my_int = 1
        Dim my_bool = True
        Dim my_float = 3.14
        Dim my_list = New Integer() {
            1,
            2,
            3
        }
        process(my_int, 42)
        process(my_bool, 7)
        process(my_float, 9)
        process(my_list, 1)
    End Sub
End Module
