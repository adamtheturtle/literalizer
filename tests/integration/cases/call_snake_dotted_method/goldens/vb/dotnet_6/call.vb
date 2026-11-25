Imports System.Collections.Generic
Module Check
    Class Http_ClientType_1_
        Public Function fetch(payload As Object) As Object
            Return Nothing
        End Function
    End Class
    Class My_AppType_0_
        Public http_client As New Http_ClientType_1_()
    End Class
    Dim my_app As New My_AppType_0_()
    Sub _calls()
        my_app.http_client.fetch("hello")
        my_app.http_client.fetch(42)
        my_app.http_client.fetch(True)
    End Sub
End Module
