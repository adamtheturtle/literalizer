Imports System.Collections.Generic
Module Check
    Function process(known_value As Object, nested_missing As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim known_value = True
        Dim unknown_value = True
        process(known_value, unknown_value)
    End Sub
End Module
