Imports System.Collections.Generic
Module Check
    Function process(value As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        process(Nothing)
        process(New Integer() {1, 2})
    End Sub
End Module
