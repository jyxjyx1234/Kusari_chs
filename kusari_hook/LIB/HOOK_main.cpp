#include <Windows.h>
#include <Shlwapi.h>
#include <fstream>
#include <iostream>
#include "HOOK_main.h"
#include "text_process.h"
#include "readconfig.h"

void CreateConsole()
{
	// �����µĿ���̨
	if (AllocConsole())
	{
		FILE* fp;
		freopen_s(&fp, "CONOUT$", "w", stdout);
		setlocale(LC_CTYPE, "zh-ch");
		// ���ÿ���̨����ҳΪUTF-8
		//_setmode(_fileno(stdout), _O_U16TEXT);
		SetConsoleOutputCP(932);
	}
}

void HOOK_main() {
	MessageBoxW(NULL, L"��������jyxjyx1234/ALyCE���������������github/2dfan��ʹ��cluade-3-5-sonnet���з��룬��������ѧϰ��������������ɵ�github��2dfan����������������", L"��Ϣ", NULL);
	rr::RConfig config;
	config.ReadConfig("hook.ini");
	if (config.ReadInt("GLOBAL", "DEBUG", 0) == 1) {
		CreateConsole();
	}

	if (config.ReadInt("TEXTPROCESS", "ENABLE", 0) == 1) {
		if (config.ReadInt("TEXTPROCESS", "REDRAWFONT", 0) == 1) {
			InstallHook_redrawfont();
		}
		InstallHook_replacetext1();
		InstallHook_replacetext2();
		InstallHook_replacetext3();
		InstallHook_replacetext4();
	}
}