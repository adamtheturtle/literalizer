Imports System.Collections.Generic
Module Check
    Class ApiType_1_
        Public Function fetch(data As Object) As Object
            Return Nothing
        End Function
    End Class
    Class ProcessType_0_
        Public api As New ApiType_1_()
    End Class
    Dim process As New ProcessType_0_()
    Sub _calls()
        process.api.fetch(New Dictionary(Of String, Object) From {{"data", "hello"}})
        process.api.fetch(New Dictionary(Of String, Object) From {{"data", 42}})
        process.api.fetch(New Dictionary(Of String, Object) From {{"data", True}})
    End Sub
End Module
