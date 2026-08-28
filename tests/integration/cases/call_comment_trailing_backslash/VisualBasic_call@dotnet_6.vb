Imports System.Collections.Generic
Module Check
    Function process(value As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        process(1)  ' trail \ .
        process(2)  ' second
    End Sub
End Module
