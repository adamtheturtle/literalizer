Imports System.Collections.Generic
Module Check
    Function process(data As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        process(New Object() {1, "x"})
    End Sub
End Module
