Imports System.Collections.Generic
Module Check
    Sub _declaration()
        ' real
        Dim my_data = New Dictionary(Of String, Object) From {
            {"key", """bang!"""}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        ' real
        my_data = New Dictionary(Of String, Object) From {
            {"key", """bang!"""}
        }
    End Sub
End Module
