Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New String() {
            "C:\path\to\file",
            "back\\slash",
            "hello \""world\""",
            "path\to ""# file"
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New String() {
            "C:\path\to\file",
            "back\\slash",
            "hello \""world\""",
            "path\to ""# file"
        }
    End Sub
End Module
