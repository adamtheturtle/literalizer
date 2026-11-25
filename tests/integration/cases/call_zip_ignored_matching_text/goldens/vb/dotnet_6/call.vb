Imports System.Collections.Generic
Module Check
    Function process(value As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        process("time.Date(2024, time.January, 15, 12, 0, 0, 0, time.UTC)")
    End Sub
End Module
