Imports System.Collections.Generic
Module Check
    Class AppType_0_
        Public Function go(first_value As Object, second_value As Object) As Object
            Return Nothing
        End Function
    End Class
    Dim app As New AppType_0_()
    Sub _calls()
        app.go(New Integer() {1}, New Integer() {2})
    End Sub
End Module
