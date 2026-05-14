Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New String() {
            "line1" & vbCrLf & "line2",
            "line1" & Chr(13) & "line2",
            Chr(1)
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New String() {
            "line1" & vbCrLf & "line2",
            "line1" & Chr(13) & "line2",
            Chr(1)
        }
    End Sub
End Module
