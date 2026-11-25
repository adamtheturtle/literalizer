Imports System.Collections.Generic
Module Check
    Function process(data As Object, count As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim MyVar = New Integer() {
            1,
            2,
            3
        }
        Dim MyOther = New Integer() {
            4,
            5,
            6
        }
        process(MyVar, 42)
        process(MyOther, 7)
    End Sub
End Module
