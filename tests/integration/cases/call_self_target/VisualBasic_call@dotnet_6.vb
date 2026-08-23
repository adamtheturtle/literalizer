Imports System.Collections.Generic
Module Check
    Function self(value As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        self("hello")
    End Sub
End Module
