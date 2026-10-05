import sys

args = sys.argv[1:]

if 1 <= len(args) <= 2:
    if len(args) == 1:
        if args[0] == 'init':
            pass
        elif args[0] in ('add', 'get'):
            print("Service must be specified after '{}'".format(args[0]))
        else:
            print('Unknown argument: {}'.format(args[0]))
    elif args[0] == 'add':
        service = args[1]
        pass
    elif args[0] == 'get':
        service = args[1]
        pass
    else:
        print('Unknown arguments: {}'.format(' '.join(args)))
elif len(args) == 0:
    print('No arguments given')
else:
    print('Too many arguments')
