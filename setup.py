import sys
import subprocess

def check_python_and_pip():
    if not sys.version_info >= (3, 6):
        print("Python 3.6 or newer is required.")
        sys.exit(1)
    try:
        import pip
    except ImportError:
        print("pip is required but not installed.")
        sys.exit(1)

def install_dependencies():
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])

def main():
    check_python_and_pip()
    install_dependencies()

if __name__ == "__main__":
    main()
