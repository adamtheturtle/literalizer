Imports System.Collections.Generic
Module Check
    Class ClientType_
        Public Function fetch(payload As Object) As Object
            Return Nothing
        End Function
    End Class
    Class AppType_
        Public client As New ClientType_()
    End Class
    Dim app As New AppType_()
    Sub _calls()
        app.client.fetch("hello")
        app.client.fetch(42)
        app.client.fetch(True)
    End Sub
End Module
