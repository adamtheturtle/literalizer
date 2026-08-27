Imports System.Collections.Generic
Module Check
    Class OuterType_0_
        Public Function inner(outer As Object, n As Object) As Object
            Return Nothing
        End Function
    End Class
    Dim outer As New OuterType_0_()
    Sub _calls()
        outer.inner(1, 2)
    End Sub
End Module
