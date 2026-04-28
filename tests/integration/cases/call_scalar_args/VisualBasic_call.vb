Imports System.Collections.Generic
Module Check
    Function process(value As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        process("hello")
        process(42)
        process(True)
    End Sub
End Module
