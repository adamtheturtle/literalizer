Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New String()() {
            New String() {"2026-01-01", "2026-01-02"},
            New String() {},
            New String() {"2026-02-03", "2026-02-04"}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New String()() {
            New String() {"2026-01-01", "2026-01-02"},
            New String() {},
            New String() {"2026-02-03", "2026-02-04"}
        }
    End Sub
End Module
