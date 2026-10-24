Imports System.Collections.Generic
Module Check
    Class FooType_0_
        Public Function class(value As Object) As Object
            Return Nothing
        End Function
    End Class
    Dim foo As New FooType_0_()
    Sub _calls()
        foo.class(1)
    End Sub
End Module
