Imports System.Collections.Generic
Module Check
    Sub _declaration()
        ' trailing
        Dim my_data = New String() {
            "a"
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        ' trailing
        my_data = New String() {
            "a"
        }
    End Sub
End Module
