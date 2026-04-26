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
    Function emit(_arg As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        emit(app.client.fetch("hello"))
        emit(app.client.fetch(42))
        emit(app.client.fetch(True))
    End Sub
End Module
