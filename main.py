import sys

from vault import init_vault, add_password, get_password

args = sys.argv[1:]

if 1 <= len(args) <= 2:
    if len(args) == 1:
        if args[0] == 'init':
            master_password = input('\nEnter new key: ')
            init_vault(master_password)
            print('Vault initialized')
        elif args[0] in ('add', 'get'):
            print("Service must be specified after '{}'".format(args[0]))
        else:
            print('Unknown argument: {}'.format(args[0]))
    elif args[0] == 'add':
        service = args[1]
        master_password = input('\nEnter key: ')
        add_result = add_password(master_password, service)
        print(add_result)
    elif args[0] == 'get':
        service = args[1]
        master_password = input('\nEnter key: ')
        get_result = get_password(master_password, service)
        print(get_result)
    else:
        print('Unknown arguments: {}'.format(' '.join(args)))
elif len(args) == 0:
    print('No arguments given')
else:
    print('Too many arguments')
