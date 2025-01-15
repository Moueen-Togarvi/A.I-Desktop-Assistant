def get_program_path(program_name: str) -> str:
    """Map common program names to their Windows paths"""
    program_paths = {
        'notepad': 'notepad.exe',
        'calculator': 'calc.exe',
        'paint': 'mspaint.exe',
        # 'word': r'C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE',
        # 'excel': r'C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE',
        'chrome': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        # 'firefox': r'C:\Program Files\Mozilla Firefox\firefox.exe',
        'code': r"C:\Users\farhan\AppData\Local\Programs\Microsoft VS Code\Code.exe"
    }
    return program_paths.get(program_name.lower())

