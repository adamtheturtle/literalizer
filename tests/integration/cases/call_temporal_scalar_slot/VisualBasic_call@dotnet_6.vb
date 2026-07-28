Imports System
Imports System.Collections.Generic
Module Check
    Function process(value As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        process(New TimeOnly(9, 30, 0))
        process("2024-01-15T00:00:00+00:00")
        process(1)
    End Sub
End Module
