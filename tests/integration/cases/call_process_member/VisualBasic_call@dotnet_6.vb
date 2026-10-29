Imports System.Collections.Generic
Module Check
    Class ProcessType_1_
        Public Function fetch(data As Object) As Object
            Return Nothing
        End Function
    End Class
    Class AppType_0_
        Public process As New ProcessType_1_()
    End Class
    Dim app As New AppType_0_()
    Sub _calls()
        app.process.fetch(New Dictionary(Of String, Object) From {{"data", "hello"}})
        app.process.fetch(New Dictionary(Of String, Object) From {{"data", 42}})
        app.process.fetch(New Dictionary(Of String, Object) From {{"data", True}})
    End Sub
End Module
