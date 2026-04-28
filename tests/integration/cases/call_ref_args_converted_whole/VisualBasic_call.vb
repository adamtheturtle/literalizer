Imports System.Collections.Generic
Module Check
    Function process(data As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim MyVar = New Integer() {
            1,
            2,
            3
        }
        process(MyVar)
    End Sub
End Module
