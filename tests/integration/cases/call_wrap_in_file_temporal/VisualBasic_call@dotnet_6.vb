Imports System.Collections.Generic
Module Check
    Function check(ts As Object, d As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        check("2024-01-15T10:30:00+00:00", New DateOnly(2024, 6, 1))
    End Sub
End Module
