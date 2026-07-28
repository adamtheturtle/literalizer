Imports System.Collections.Generic
Module Check
    Function process(data As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim known_value = 1
        Dim unknown_value = New Object() {}
        process(unknown_value)
    End Sub
End Module
