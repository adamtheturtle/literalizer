Imports System.Collections.Generic
Module Check
    Function process(v As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim my_str = "a""b"
        process(my_str)
    End Sub
End Module
