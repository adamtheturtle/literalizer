Imports System.Collections.Generic
Module Check
    Class WorkerType_1_
        Public Function process(values As Object, count As Object) As Object
            Return Nothing
        End Function
    End Class
    Class ApiType_0_
        Public worker As New WorkerType_1_()
    End Class
    Dim api As New ApiType_0_()
    Sub _calls()
        api.worker.process(New Object() {1, New Dictionary(Of String, Object) From {}}, 42)
        api.worker.process(New Object() {2, New Dictionary(Of String, Object) From {{"x", "s"}}}, 43)
    End Sub
End Module
