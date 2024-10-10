import sys, os

USAGE = 'USAGE\n\t{binary_name}\tfilename\n'.format(binary_name=os.path.basename(sys.argv[0]))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(USAGE, end='')
        sys.exit()

    script_vars = {
        'CASSANDRA_KEYSPACE': os.environ.get('CASSANDRA_KEYSPACE'),
        'FETCHING_INFO_TABLE': os.environ.get('FETCHING_INFO_TABLE')
    }

    filename = sys.argv[1]
    with open(filename) as script_file:
        content = script_file.read()
        
        for var in script_vars:
            content = content.replace('<{}>'.format(var), script_vars[var])
        
        print(content)
