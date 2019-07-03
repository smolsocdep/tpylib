del form_reference.bak
del form_ref_edit.bak
D:\work\src\pgcontracts\environment\Scripts\python.exe -m PyQt5.uic.pyuic form_reference.ui -o form_reference.py
D:\work\src\pgcontracts\environment\Scripts\python.exe -m PyQt5.uic.pyuic form_ref_edit.ui -o form_ref_edit.py
rem 
D:\work\src\pgcontracts\environment\Scripts\python.exe -m PyQt5.pyrcc_main tpylib.qrc -o tpylib_rc.py
rem 
D:\work\src\pgcontracts\environment\Scripts\python.exe D:\work\src\pgcontracts\src\forms\tune_forms.py form_reference.py tpylib
D:\work\src\pgcontracts\environment\Scripts\python.exe D:\work\src\pgcontracts\src\forms\tune_forms.py form_ref_edit.py tpylib

