Imports System.Collections.Generic
Module Check
    Class MgrType_
        Public Function op(operation As Object) As Object
            Return Nothing
        End Function
    End Class
    Class AppType_
        Public mgr As New MgrType_()
    End Class
    Dim app As New AppType_()
    Sub _calls()
        app.mgr.op(New Dictionary(Of String, Object) From {{"type", "create"}, {"pr_id", "pr_1"}, {"draft", True}})
        app.mgr.op(New Dictionary(Of String, Object) From {{"type", "create"}, {"pr_id", "pr_2"}})
    End Sub
End Module
