import ConfigParser
import pickle

from netflix import connection as n_connection
from netflix import parser as n_parser

def main():
    config = ConfigParser.SafeConfigParser()
    config.read('config')

    email = config.get('netflix_parser', 'email')
    password = config.get('netflix_parser', 'password')

    n_conn = n_connection.NetflixConnection(email, password)
    n_conn.login()
    viewing_data = n_conn.get_viewing_activity()

    n_data = n_parser.parseData(viewing_data)
    #print n_data.text_tables()
    #print n_data.all_data()
    with open('data.pickle', 'w') as f:
        pickle.dump(n_data, f)
    n_data.line_plot()

if __name__ == '__main__':
    main()
