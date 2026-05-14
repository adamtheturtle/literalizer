Imports System.Collections.Generic
Module Check
    Class ClientType_2_
        Public Function post(data As Object) As Object
            Return Nothing
        End Function
    End Class
    Class ApiType_1_
        Public client As New ClientType_2_()
    End Class
    Class ObjType_0_
        Public api As New ApiType_1_()
    End Class
    Dim obj As New ObjType_0_()
    Sub _calls()
        obj.api.client.post("hello")
        obj.api.client.post(42)
        obj.api.client.post(True)
    End Sub
End Module
