Imports System.Collections.Generic
Module Check
    Class ClientType_
        Public Function post(data As Object) As Object
            Return Nothing
        End Function
    End Class
    Class ApiType_
        Public client As New ClientType_()
    End Class
    Class ObjType_
        Public api As New ApiType_()
    End Class
    Dim obj As New ObjType_()
    Sub _calls()
        obj.api.client.post("hello")
        obj.api.client.post(42)
        obj.api.client.post(True)
    End Sub
End Module
