@echo off
chcp 65001
rem 作为命令行启动的快捷入口
rem 可以使用 envirment.bat 使用本地复制的python环境
rem 如果在conda 环境中使用，应注释掉 call envirment.bat
:start_env
title 听写启动器 - 配置环境
cls
set "envsel=x"
echo ---------------------------------------
echo - 1 - 执行 environment.bat 配置环境
echo - 2 - 不更改环境配置继续运行.
echo - 3 - 激活conda环境，手动运行(exit退出)
echo - 4 - 打开文件夹.
echo - 5 - Git
echo ---------------------------------------
set /p "envsel=请选择Python运行环境: "
if %envsel%==1 (
    call environment.bat 
) else if %envsel%==2 (
	cls
    echo 环境配置未更改
) else if %envsel%==3 ( 
	cls
	title Poe/Slack 启动器 -conda环境 输入exit 退出
    %windir%\System32\cmd.exe "/K" F:\Installed_Soft\Anaconda3\Scripts\activate.bat F:\Installed_Soft\Anaconda3\envs\ClaudeSlack
	echo 已退出conda环境
	pause
	goto start_env
rem	exit
) else if %envsel%==4 (
	explorer .\
	goto start_env
) else if %envsel%==5 (
	call set_git.bat
	goto start_env
) else (
	cls
    echo 输入有误,请重新输入!
    goto start_env
)

setlocal enabledelayedexpansion
:start_run
echo ------------------------------
title 听写启动器
echo start now...
echo ------------------------------
PYTHON main_ui.py
echo ------------------------------
echo 执行完毕，按任意键返回
pause
cls
goto start_env
rem 使用exit 可以退出，即使快捷方式有参数 "K"
rem exit
rem exit /b
endlocal
