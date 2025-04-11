<div align="center">
<img src="readme_assets/ImpWizLogo.png" alt="ImpWiz Logo" width="200"/>
</div>

**ImpWiz** (Import Wizard) is the ultimate Python import tool designed to take the chaos out of dependency management. It scans your codebase, detects all used imports, and checks for unused or missing ones.

## Key Features
### General
#### Generate `requirements.txt` from used imports

Generates a minimal `requirements.txt` based only on the imports actually used:
```bash
impwiz [-r | --requirements] > requirements.txt
```
### Venv
Show imports in virtual environment.
```bash
impwiz [--venv]
```
#### Show difference between used imports and dependencies
Displays declared dependencies that aren't used in the code:
```bash
impwiz [--venv] [-d | --difference]
```

#### Show intersection of used imports and dependencies
Lists used imports and their matching versions from `venv`:
```bash
impwiz [--venv] [-i | --intersection]
```
### Poetry
#### Show difference between used imports and dependencies
Displays declared dependencies that aren't used in the code:
```bash
impwiz [-p | --poetry] [-d | --difference]
```

#### Show intersection of used imports and dependencies
Lists used imports and their matching versions from `poetry.lock`:
```bash
impwiz [-p | --poetry] [-i | --intersection]
```

### Help
Displays help message:
```bash
impwiz [-h | --help]
```
