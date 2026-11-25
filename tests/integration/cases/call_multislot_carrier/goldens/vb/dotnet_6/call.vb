Imports System.Collections.Generic
Module Check
    Function process(value As Object, extra As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        process(1, "hello")
        process("two", False)
        process(3.5, Nothing)
    End Sub
End Module
