Imports System.Collections.Generic
Module Check
    Function process(data As Object, count As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim my_ints = New Integer() {
            1,
            2,
            3
        }
        Dim my_strings = New String() {
            "a",
            "b"
        }
        process(my_ints, 42)
        process(my_strings, 7)
    End Sub
End Module
