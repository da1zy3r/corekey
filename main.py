import argparse

from vault import init_vault, add_password, get_password, get_list

def cmd_init(args):
    master_password = input('\nEnter new key: ')
    init_vault(master_password)
    print('Vault initialized')

def cmd_list(args):
    master_password = input('\nEnter key: ')
    services = get_list(master_password)
    if not services:
        print('No services added')
    else:
        print('Saved services:')
        for service in services:
            print('- {}'.format(service))

def cmd_add(args):
    master_password = input('\nEnter key: ')
    add_result = add_password(master_password, args.service)
    print(add_result)

def cmd_get(args):
    master_password = input('\nEnter key: ')
    get_result = get_password(master_password, args.service)
    print(get_result)

def main():
    parser = argparse.ArgumentParser(prog='ck', description='corekey, a password manager')
    subparsers = parser.add_subparsers(dest='command', required=True)
    init_parser = subparsers.add_parser('init', help='Initialize the vault')
    init_parser.set_defaults(func=cmd_init)
    list_parser = subparsers.add_parser('list', help='List saved services')
    list_parser.set_defaults(func=cmd_list)
    add_parser = subparsers.add_parser('add', help='Generate and save a password')
    add_parser.add_argument('service', help='Service name')
    add_parser.set_defaults(func=cmd_add)
    get_parser = subparsers.add_parser('get', help='Retrieve a saved password')
    get_parser.add_argument('service', help='Service name')
    get_parser.set_defaults(func=cmd_get)
    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
