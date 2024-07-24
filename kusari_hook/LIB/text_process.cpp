#include <windows.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <map>
#include <codecvt>
#include <locale>
#include <vector>
#include "text_process.h"

DWORD originalFuncAddr1;
DWORD returnAddress1;
DWORD originalFuncAddr2;
DWORD returnAddress2;
DWORD originalFuncAddr3;
DWORD returnAddress3;
DWORD originalFuncAddr4;
DWORD returnAddress4;
DWORD originalFuncAddr5;
DWORD returnAddress5;

std::vector<char> fileContent;

std::map<std::string, std::string> readKeyValuePairsFromFile(const std::string& filename) {
    std::map<std::string, std::string> result;
    std::ifstream file(filename, std::ios::in | std::ios::binary);

    if (!file.is_open()) {
        std::cerr << "Error: Unable to open file " << filename << std::endl;
        return result;
    }

    std::string line;
    while (std::getline(file, line)) {
        size_t equalPos = line.find('=');
        if (equalPos != std::string::npos) {
            std::string key = line.substr(0, equalPos);
            std::string value = line.substr(equalPos + 1);

            // 移除前后的空白字符
            key.erase(0, key.find_first_not_of(" \t"));
            key.erase(key.find_last_not_of(" \t") + 1);
            value.erase(0, value.find_first_not_of(" \t"));
            value.erase(value.find_last_not_of(" \t") + 1);

            result[key] = value;
        }
    }
    printf("Read trans: sucess!");
    file.close();
    return result;
}

void WriteToFile(const char* text, bool addAtSign)
{
    std::ofstream file("output.txt", std::ios::app);
    if (file.is_open())
    {
        if (addAtSign)
            file << "@";
        file << text << std::endl;
        file.close();
    }
}

std::map<std::string, std::string> replacementMap = readKeyValuePairsFromFile("trans.dat");

void replacetext() {
    char buffer[256];  // 假设字符串最长为 255 字符
    SIZE_T bytesRead;

    // 读取内存中的字符串
    if (ReadProcessMemory(GetCurrentProcess(), (LPCVOID)0x4DDF10, buffer, sizeof(buffer) - 1, &bytesRead))
    {
        buffer[bytesRead] = '\0';  // 确保字符串以 null 结尾
        std::string originalString(buffer);

        // 在映射表中查找并替换
        if (replacementMap.find(originalString) != replacementMap.end())
        {
            std::string newString = replacementMap[originalString];

            // 写回内存
            WriteProcessMemory(GetCurrentProcess(), (LPVOID)0x4DDF10, newString.c_str(), newString.length() + 1, NULL);
        }
        else {
            std::ofstream file("output.txt", std::ios::app);
            if (file.is_open())
            {
                file << originalString << std::endl;
                file.close();
            }
        }
    }
}

void __declspec(naked) HookFunction_replacetext1() {
    __asm
    {
        pushad  // 保存所有寄存器
        pushfd  // 保存标志寄存器
        
        call replacetext

        popfd   // 恢复标志寄存器
        popad   // 恢复所有寄存器

        // 执行原始代码
        pop edi
        mov byte ptr ds : [ecx + ebp * 1] , 0x00

        // 跳回原始代码的下一条指令
        jmp dword ptr[returnAddress1]
    }
}

void __declspec(naked) HookFunction_replacetext2() {
    __asm
    {
        pushad  // 保存所有寄存器
        pushfd  // 保存标志寄存器

        call replacetext

        popfd   // 恢复标志寄存器
        popad   // 恢复所有寄存器

        // 执行原始代码
        lea esp, ss: [esp]

        // 跳回原始代码的下一条指令
        jmp dword ptr[returnAddress2]
    }
}

void __declspec(naked) HookFunction_replacetext3() {
    __asm
    {
        pushad  // 保存所有寄存器
        pushfd  // 保存标志寄存器

        call replacetext

        popfd   // 恢复标志寄存器
        popad   // 恢复所有寄存器

        // 执行原始代码
        mov dword ptr ds : [0x004E2020] , 0x4DDF10

        // 跳回原始代码的下一条指令
        jmp dword ptr[returnAddress3]
    }
}

void __declspec(naked) HookFunction_replacetext4() {
    __asm
    {
        pushad  // 保存所有寄存器
        pushfd  // 保存标志寄存器

        call replacetext

        popfd   // 恢复标志寄存器
        popad   // 恢复所有寄存器

        // 执行原始代码
        mov ecx, 0x00

        // 跳回原始代码的下一条指令
        jmp dword ptr[returnAddress4]
    }
}

void InstallHook_replacetext1() {
    DWORD oldProtect;

    originalFuncAddr1 = 0x403A5B;  
    returnAddress1 = 0x403A60;

    // 修改内存保护
    VirtualProtect((LPVOID)originalFuncAddr1, 5, PAGE_EXECUTE_READWRITE, &oldProtect);

    // 写入跳转指令
    *(BYTE*)originalFuncAddr1 = 0xE9;  // JMP
    *(DWORD*)(originalFuncAddr1 + 1) = (DWORD)HookFunction_replacetext1 - originalFuncAddr1 - 5;

    // 恢复内存保护
    VirtualProtect((LPVOID)originalFuncAddr1, 5, oldProtect, &oldProtect);
}

void InstallHook_replacetext2() {// backlog汉化
    DWORD oldProtect;

    originalFuncAddr2 = 0x4012A9;
    returnAddress2 = 0x4012b0;

    // 修改内存保护
    VirtualProtect((LPVOID)originalFuncAddr2, 5, PAGE_EXECUTE_READWRITE, &oldProtect);

    // 写入跳转指令
    *(BYTE*)originalFuncAddr2 = 0xE9;  // JMP
    *(DWORD*)(originalFuncAddr2 + 1) = (DWORD)HookFunction_replacetext2 - originalFuncAddr2 - 5;

    // 恢复内存保护
    VirtualProtect((LPVOID)originalFuncAddr2, 5, oldProtect, &oldProtect);
}

void InstallHook_replacetext3() {
    DWORD oldProtect;

    originalFuncAddr3 = 0x404606;
    returnAddress3 = 0x404610;

    // 修改内存保护
    VirtualProtect((LPVOID)originalFuncAddr3, 5, PAGE_EXECUTE_READWRITE, &oldProtect);

    // 写入跳转指令
    *(BYTE*)originalFuncAddr3 = 0xE9;  // JMP
    *(DWORD*)(originalFuncAddr3 + 1) = (DWORD)HookFunction_replacetext3 - originalFuncAddr3 - 5;

    // 恢复内存保护
    VirtualProtect((LPVOID)originalFuncAddr3, 5, oldProtect, &oldProtect);
}

void InstallHook_replacetext4() {
    DWORD oldProtect;

    originalFuncAddr4 = 0x403a3a;
    returnAddress4 = 0x403a3f;

    // 修改内存保护
    VirtualProtect((LPVOID)originalFuncAddr4, 5, PAGE_EXECUTE_READWRITE, &oldProtect);

    // 写入跳转指令
    *(BYTE*)originalFuncAddr4 = 0xE9;  // JMP
    *(DWORD*)(originalFuncAddr4 + 1) = (DWORD)HookFunction_replacetext4 - originalFuncAddr4 - 5;

    // 恢复内存保护
    VirtualProtect((LPVOID)originalFuncAddr4, 5, oldProtect, &oldProtect);
}

void __declspec(naked) HookFunction_redrawfont() {
    __asm
    {
        // 保存寄存器状态
        push edx
        push eax
        

        // 使用文件内容的起始地址替换原始的0x619010
        mov eax, dword ptr[fileContent]
        add edx, eax

        // 恢复寄存器状态
        pop eax
        mov al, byte ptr[edx]
        pop edx

        // 跳回到原始代码
        jmp returnAddress5
    }
}


bool ReadFile(const char* filename)
{
    std::ifstream file(filename, std::ios::binary);
    if (!file)
        return false;

    file.seekg(0, std::ios::end);
    size_t fileSize = file.tellg();
    file.seekg(0, std::ios::beg);

    fileContent.resize(fileSize);
    file.read(fileContent.data(), fileSize);

    return true;
}

void InstallHook_redrawfont() {
    ReadFile("MAINFONT.FNT");
    DWORD oldProtect;

    originalFuncAddr5 = 0x416969;  
    returnAddress5 = 0x41696f;  

    // 修改内存保护
    VirtualProtect((LPVOID)originalFuncAddr5, 5, PAGE_EXECUTE_READWRITE, &oldProtect);

    // 写入跳转指令
    *(BYTE*)originalFuncAddr5 = 0xE9;  // JMP
    *(DWORD*)(originalFuncAddr5 + 1) = (DWORD)HookFunction_redrawfont - originalFuncAddr5 - 5;
    *(BYTE*)(originalFuncAddr5 + 5) = 0x90;
    // 恢复内存保护
    VirtualProtect((LPVOID)originalFuncAddr5, 5, oldProtect, &oldProtect);
}