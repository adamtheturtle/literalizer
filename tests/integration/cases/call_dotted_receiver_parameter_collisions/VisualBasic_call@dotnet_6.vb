Imports System.Collections.Generic
Module Check
    Class WorkerType_1_
        Public Function process(self As Object, self_ As Object) As Object
            Return Nothing
        End Function
    End Class
    Class ApiType_0_
        Public worker As New WorkerType_1_()
    End Class
    Dim api As New ApiType_0_()
    Sub _calls()
        api.worker.process(New Dictionary(Of String, Object) From {}, New Dictionary(Of String, Object) From {})
    End Sub
End Module
