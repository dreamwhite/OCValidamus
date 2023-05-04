import os
import pathlib
import plistlib
import sys


FOLDERS_FILES_CHECK = ("EFI", "EFI/OC", "EFI/OC/config.plist")


class Colors():
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class OCValidamus:
    def __init__(self):
        self.pl: dict = None

        self.errors: int = 0

    def load_config(self) -> dict:
        path = pathlib.Path(".")

        for p in FOLDERS_FILES_CHECK:
            if not (path / p).exists():
                raise FileNotFoundError(
                    f"{Colors.FAIL}{p} not found{Colors.ENDC}"
                )

        with open("EFI/OC/config.plist", "rb") as f:
            return plistlib.load(f)

    def check_acpi(self):
        acpi = self.pl["ACPI"]["Add"]

        if not acpi:
            print(f"\t{Colors.WARNING}There are no ACPI{Colors.ENDC}")
            return

        for ssdt in acpi:
            if ssdt["Enabled"]:
                print(
                    f"Checking {Colors.OKCYAN}{ssdt['Path']}{Colors.ENDC} {Colors.UNDERLINE}({ssdt['Comment']}){Colors.ENDC}"
                )

                if os.path.exists(f"EFI/OC/ACPI/{ssdt['Path']}"):
                    print(
                        f"\t- {Colors.OKGREEN}{ssdt['Path']}{Colors.ENDC} exists"
                    )
                else:
                    print(
                        f"\t- {Colors.FAIL}{ssdt['Path']}{Colors.ENDC} does not exists"
                    )
                    self.errors += 1
            else:
                print(
                    f"Skipping {Colors.WARNING}{ssdt['Path']}{Colors.ENDC} {Colors.UNDERLINE}({ssdt['Comment']}){Colors.ENDC} as it's disabled"
                )

    def check_driver(self):
        driver = self.pl["UEFI"]["Drivers"]

        if not driver:
            print(f"\t{Colors.WARNING}There are no drivers{Colors.ENDC}")
            return

        for driver in driver:
            if driver["Enabled"]:
                print(
                    f"Checking {Colors.OKCYAN}{driver['Path']}{Colors.ENDC} {Colors.UNDERLINE}({driver['Comment']}){Colors.ENDC}"
                )

                if os.path.exists(f'EFI/OC/Drivers/{driver["Path"]}'):
                    print(
                        f"\t- {Colors.OKGREEN}{driver['Path']}{Colors.ENDC} exists"
                    )
                else:
                    print(
                        f"\t- {Colors.FAIL}{driver['Path']}{Colors.ENDC} does not exist"
                    )
                    self.errors += 1
            else:
                print(
                    f"Skipping {Colors.WARNING}{driver['Path']}{Colors.ENDC} {Colors.UNDERLINE}({driver['Comment']}){Colors.ENDC} as it's disabled"
                )

    def check_kexts(self):
        kexts = self.pl["Kernel"]["Add"]

        if not kexts:
            print(f"\t{Colors.WARNING}There are no kexts{Colors.ENDC}")
            return

        for kext in kexts:
            if kext["Enabled"]:
                print(
                    f"Checking {Colors.OKCYAN}{kext['BundlePath']}{Colors.ENDC} {Colors.UNDERLINE}({kext['Comment']}){Colors.ENDC}"
                )

                path = pathlib.Path(f"EFI/OC/Kexts/{kext['BundlePath']}")

                if path.exists():
                    print(f"\t- {Colors.OKGREEN}{path}{Colors.ENDC} exist")
                else:
                    print(
                        f"\t- {Colors.FAIL}{path}{Colors.ENDC} does not exist"
                    )
                    self.errors += 1

                for x in filter(
                    None, (kext["ExecutablePath"], kext["PlistPath"])
                ):
                    if (path / x).exists():
                        print(f"\t\t- {Colors.OKGREEN}{x}{Colors.ENDC} exists")
                    else:
                        print(
                            f"\t\t- {Colors.FAIL}{x}{Colors.ENDC} does not exists"
                        )
                        self.errors += 1
            else:
                print(
                    f"Skipping {Colors.WARNING}{kext['BundlePath']}{Colors.ENDC} {Colors.UNDERLINE}({kext['Comment']}){Colors.ENDC} as it's disabled"
                )

    def check_tools(self):
        tools = self.pl["Misc"]["Tools"]

        if not tools:
            print(f"\t{Colors.WARNING}There are no tools{Colors.ENDC}")
            return

        for tool in tools:
            if tool["Enabled"]:
                print(
                    f"Checking {Colors.OKCYAN}{tool['Path']}{Colors.ENDC} {Colors.UNDERLINE}({tool['Comment']}){Colors.ENDC}"
                )

                if os.path.exists(f'EFI/OC/Tools/{tool["Path"]}'):
                    print(
                        f"""\t - {Colors.OKGREEN}{tool['Path']}{Colors.ENDC} exists"""
                    )
                else:
                    print(
                        f"""\t - {Colors.FAIL}{tool['Path']}{Colors.ENDC} does not exists"""
                    )
                    self.errors += 1
            else:
                print(
                    f"Skipping {Colors.WARNING}{tool['Path']}{Colors.ENDC} {Colors.UNDERLINE}({tool['Comment']}){Colors.ENDC} as it's disabled"
                )

    def validate(self):
        self.pl: dict = self.load_config()

        print(f"\n{Colors.HEADER}---CHECK ACPI---{Colors.ENDC}")
        self.check_acpi()
        print(f"\n{Colors.HEADER}---CHECK Drivers---{Colors.ENDC}")
        self.check_driver()
        print(f"\n{Colors.HEADER}---CHECK Kexts---{Colors.ENDC}")
        self.check_kexts()
        print(f"\n{Colors.HEADER}---CHECK Tools---{Colors.ENDC}")
        self.check_tools()

        if self.errors:
            print(
                f"\n{Colors.FAIL}Found {self.errors} issue requiring attention.{Colors.ENDC}"
            )
        else:
            print(f"\n{Colors.OKGREEN}No issues found{Colors.ENDC}")

        sys.exit(1 if self.errors else 0)


if __name__ == "__main__":
    print(
        f"""{Colors.HEADER}
 ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄   ▄▄ ▄▄▄▄▄▄ ▄▄▄     ▄▄▄ ▄▄▄▄▄▄  ▄▄▄▄▄▄ ▄▄   ▄▄ ▄▄   ▄▄ ▄▄▄▄▄▄▄ 
█       █       █  █ █  █      █   █   █   █      ██      █  █▄█  █  █ █  █       █
█   ▄   █       █  █▄█  █  ▄   █   █   █   █  ▄    █  ▄   █       █  █ █  █  ▄▄▄▄▄█
█  █ █  █     ▄▄█       █ █▄█  █   █   █   █ █ █   █ █▄█  █       █  █▄█  █ █▄▄▄▄▄ 
█  █▄█  █    █  █       █      █   █▄▄▄█   █ █▄█   █      █       █       █▄▄▄▄▄  █
█       █    █▄▄ █     ██  ▄   █       █   █       █  ▄   █ ██▄██ █       █▄▄▄▄▄█ █
█▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█ █▄▄▄█ █▄█ █▄▄█▄▄▄▄▄▄▄█▄▄▄█▄▄▄▄▄▄██▄█ █▄▄█▄█   █▄█▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█

\t\t\t\t\t\t\tMade with ♡ by dreamwhite
    {Colors.ENDC}"""
    )

    OCValidamus().validate()
