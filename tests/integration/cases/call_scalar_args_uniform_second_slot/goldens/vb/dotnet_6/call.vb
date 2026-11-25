Imports System.Collections.Generic
Module Check
    Function process(value As Object, label As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        process("hello", "a")
        process(42, "b")
        process(True, "c")
    End Sub
End Module
