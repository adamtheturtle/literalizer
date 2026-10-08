Imports System.Collections.Generic
Module Check
    Function capture(__proto__ As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        capture(1)
    End Sub
End Module
