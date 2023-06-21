chcp 65001
@echo off
rem title 环境配置和快捷索引
cls
set "WINPYDIR=%~dp0\..\chatRecorder_Env"
IF EXIST %WINPYDIR% (
echo 使用本地集成的Python解释器
echo Dir: %WINPYDIR%
rem echo ------------------------
set "PATH=%WINPYDIR%\;%WINPYDIR%\DLLs;%WINPYDIR%\Scripts;%PATH%;"
set "PYTHON=%WINPYDIR%\python.exe "
goto end
) ELSE (
echo 路径不存在，继续使用当前默认的python解释器
rem echo ----------------------------------------
set "PYTHON=python.exe "
)
:end
