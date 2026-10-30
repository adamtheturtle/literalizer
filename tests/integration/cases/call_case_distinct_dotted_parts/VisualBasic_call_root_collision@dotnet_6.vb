Imports System.Collections.Generic
Module Check
    Class FooType_1_
        Public Function bar(x As Object) As Object
            Return Nothing
        End Function
    End Class
    Class FooType_0_
        Public Foo As New FooType_1_()
    End Class
    Dim foo As New FooType_0_()
    Sub _calls()
        foo.Foo.bar(New Integer() {1})
    End Sub
End Module
