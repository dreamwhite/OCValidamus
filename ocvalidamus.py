import plistlib
import os
import sys


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class OCValidamus:
    def __init__(self):
        with open('EFI/OC/config.plist', 'rb') as f:
            self.pl = plistlib.load(f)

        self.errors = 0

        self.check_acpi()
        self.check_driver()
        self.check_kexts()
        self.check_tools()

        match self.errors:
            case 0:
                print(f"\n{Colors.OKGREEN}No issues found{Colors.ENDC}")
            case 1:
                print(f"\n{Colors.FAIL}Found {self.errors} issue requiring attention.{Colors.ENDC}")
            case _:
                print(f"\n{Colors.FAIL}Found {self.errors} issues requiring attention.{Colors.ENDC}")

        sys.exit(1 if self.errors != 0 else self.errors)

    def check_acpi(self):
        print(f"\n{Colors.HEADER}---CHECK ACPI---{Colors.ENDC}")
        for ssdt in self.pl['ACPI']['Add']:
            print(f"Checking {Colors.OKCYAN}{ssdt['Path']}{Colors.ENDC} ({ssdt['Comment']})")
            if os.path.exists(f"EFI/OC/ACPI/{ssdt['Path']}"):
                print(f"\t- {Colors.OKGREEN}{ssdt['Path']}{Colors.ENDC} exists")
            else:
                print(f"\t- {Colors.FAIL}{ssdt['Path']}{Colors.ENDC} does not exists")
                self.errors += 1

    def check_driver(self):
        print(f"\n{Colors.HEADER}---CHECK Drivers---{Colors.ENDC}")
        for driver in self.pl['UEFI']['Drivers']:
            print(f'Checking {Colors.OKCYAN}{driver["Path"]}{Colors.ENDC} ({driver["Comment"]})')
            if os.path.exists(f'EFI/OC/Drivers/{driver["Path"]}'):
                print(f"\t- {Colors.OKGREEN}{driver['Path']}{Colors.ENDC} exists")
            else:
                print(f"\t- {Colors.FAIL}{driver['Path']}{Colors.ENDC} does not exist")
                self.errors += 1

    def check_kexts(self):
        print(f"\n{Colors.HEADER}---CHECK Kexts---{Colors.ENDC}")
        for kext in self.pl['Kernel']['Add']:
            print(f"Checking {Colors.OKCYAN}{kext['BundlePath']}{Colors.ENDC} ({kext['Comment']})")

            if os.path.exists(f'EFI/OC/Kexts/{kext["BundlePath"]}'):
                print(f"\t- {Colors.OKGREEN}{kext['BundlePath']}{Colors.ENDC} exist")
            else:
                print(f"\t- {Colors.FAIL}{kext['BundlePath']}{Colors.ENDC} does not exist")
                self.errors += 1

            if os.path.exists(f'EFI/OC/Kexts/{kext["BundlePath"]}/{kext["ExecutablePath"]}'):
                print(f"\t\t- {Colors.OKGREEN}{kext['ExecutablePath']}{Colors.ENDC} exists")
            else:
                print(f"\t\t- {Colors.FAIL}{kext['ExecutablePath']}{Colors.ENDC} does not exists")
                self.errors += 1

            if os.path.exists(f'EFI/OC/Kexts/{kext["BundlePath"]}/{kext["PlistPath"]}'):
                print(f"\t\t- {Colors.OKGREEN}{kext['PlistPath']}{Colors.ENDC} exists")
            else:
                print(f"\t\t- {Colors.FAIL}{kext['PlistPath']}{Colors.ENDC} does not exists")
                self.errors += 1

    def check_tools(self):
        print(f"\n{Colors.HEADER}---CHECK Tools---{Colors.ENDC}")
        if self.pl['Misc']['Tools'] != list():
            for tool in self.pl['Misc']['Tools']:
                print(f"Checking {Colors.OKCYAN}{tool['Path']}{Colors.ENDC} ({tool['Comment']})")
                if os.path.exists(f'EFI/OC/Tools/{tool["Path"]}'):
                    print(f"""\t - {Colors.OKGREEN}{tool['Path']}{Colors.ENDC} exists""")
                else:
                    print(f"""\t - {Colors.FAIL}{tool['Path']}{Colors.ENDC} does not exists""")
                    self.errors += 1

        else:
            print(f'{Colors.WARNING}There are no tools{Colors.ENDC}')


if __name__ == '__main__':
    print(f"""{Colors.HEADER}
 ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄   ▄▄ ▄▄▄▄▄▄ ▄▄▄     ▄▄▄ ▄▄▄▄▄▄  ▄▄▄▄▄▄ ▄▄   ▄▄ ▄▄   ▄▄ ▄▄▄▄▄▄▄ 
█       █       █  █ █  █      █   █   █   █      ██      █  █▄█  █  █ █  █       █
█   ▄   █       █  █▄█  █  ▄   █   █   █   █  ▄    █  ▄   █       █  █ █  █  ▄▄▄▄▄█
█  █ █  █     ▄▄█       █ █▄█  █   █   █   █ █ █   █ █▄█  █       █  █▄█  █ █▄▄▄▄▄ 
█  █▄█  █    █  █       █      █   █▄▄▄█   █ █▄█   █      █       █       █▄▄▄▄▄  █
█       █    █▄▄ █     ██  ▄   █       █   █       █  ▄   █ ██▄██ █       █▄▄▄▄▄█ █
█▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█ █▄▄▄█ █▄█ █▄▄█▄▄▄▄▄▄▄█▄▄▄█▄▄▄▄▄▄██▄█ █▄▄█▄█   █▄█▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█

\t\t\t\t\t\t\tMade with ♡ by dreamwhite
    {Colors.ENDC}""")
    OCValidamus()
