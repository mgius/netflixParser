import ConfigParser

from netflix import connection as n_connection
from netflix import parser as n_parser

def main():
    config = ConfigParser.SafeConfigParser()
    config.read('config')

    email = config.get('netflix_parser', 'email')
    password = config.get('netflix_parser', 'password')

    n_conn = n_connection.NetflixConnection(email, password)
    n_conn.login()
    data = n_conn.get_viewing_activity()

    n_parser.parseData(data)

if __name__ == '__main__':
    main()
