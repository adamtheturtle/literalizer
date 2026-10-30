Imports System.Collections.Generic
Module Check
    Class FooType_2_
        Public Function bar(x As Object) As Object
            Return Nothing
        End Function
    End Class
    Class FooType_1_
        Public Foo As New FooType_2_()
    End Class
    Class AType_0_
        Public foo As New FooType_1_()
    End Class
    Dim a As New AType_0_()
    Sub _calls()
        Dim my_data = a.foo.Foo.bar(New Integer() {1})
    End Sub
End Module
