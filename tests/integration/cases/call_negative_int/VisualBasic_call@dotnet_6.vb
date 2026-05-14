Imports System.Collections.Generic
Module Check
    Function process(value As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        process(-1)
        process(-2)
        process(-3)
    End Sub
End Module
