# OCValidamus

Validate your OpenCore BSP by checking the existence of:

    - ACPI
    - Drivers
    - Kexts
    - Tools


## Requirements

- Python 3.10
## Usage

Copy `ocvalidamus.py` outside the EFI directory<br>

e.g.

```
├── EFI
│   ├── BOOT
│   └── OC
├── ocvalidamus.py
```
Run `python3 ocvalidamus.py` and check the output of the terminal output


# Credits

- [acidanthera](https://github.com/acidanthera) for [OpenCorePkg and ocvalidate](https://github.com/acidanthera/OpenCorePkg)
