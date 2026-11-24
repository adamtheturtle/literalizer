Imports System.Collections.Generic
Module Check
    Class ClientType_1_
        Public Function fetch(value As Object) As Object
            Return Nothing
        End Function
    End Class
    Class AppType_0_
        Public client As New ClientType_1_()
    End Class
    Dim app As New AppType_0_()
    Sub _calls()
        app.client.fetch("hello")
        app.client.fetch("world")
    End Sub
End Module
