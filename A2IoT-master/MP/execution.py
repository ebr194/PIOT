# Main function.
import socketConnection
from masterMenu import Menu

def main():
    #socketConnection.queryConnect()
    username = 'erelf'
    email = 'erelf@gmail.com'
    Menu().userMenu(username, email)
# Execute program.
if __name__ == "__main__":
    main()
