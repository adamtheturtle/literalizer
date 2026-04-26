Imports System.Collections.Generic
Module Check
    Class MgrType_1_
        Public Function op(operation As Object) As Object
            Return Nothing
        End Function
    End Class
    Class AppType_0_
        Public mgr As New MgrType_1_()
    End Class
    Dim app As New AppType_0_()
    Sub _calls()
        app.mgr.op(New Dictionary(Of String, Object) From {{"type", "create"}, {"pr_id", "pr_1"}, {"draft", True}})
        app.mgr.op(New Dictionary(Of String, Object) From {{"type", "create"}, {"pr_id", "pr_2"}})
    End Sub
End Module
