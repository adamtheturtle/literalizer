Imports System.Collections.Generic
Module Check
    Function process(data As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim unknown_value = New Integer() {
            1
        }
        process(unknown_value)
    End Sub
End Module
