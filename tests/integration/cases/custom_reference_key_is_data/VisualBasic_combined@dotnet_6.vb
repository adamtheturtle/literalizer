Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Dictionary(Of String, Object) From {
            {"reference", "whole"}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Dictionary(Of String, Object) From {
            {"reference", "whole"}
        }
    End Sub
End Module
