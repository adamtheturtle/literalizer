Imports System.Collections.Generic
Module Check
    Class ApiType_0_
        Public Function process(self As Object) As Object
            Return Nothing
        End Function
    End Class
    Dim api As New ApiType_0_()
    Sub _calls()
        api.process(New Dictionary(Of String, Object) From {})
    End Sub
End Module
