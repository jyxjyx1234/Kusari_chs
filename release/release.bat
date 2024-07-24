copy ..\kusari_hook\Release\*.dll dlls\
copy ..\README.md .\
del release.rar
rar a release.rar -m0 trans.dat
rar a release.rar -m0 MAINFONT.FNT
rar a release.rar -m0 README.md 
rar a release.rar -m0 dlls\*
rar a release.rar -m0 image
rar a release.rar -m0 hook.ini
pause