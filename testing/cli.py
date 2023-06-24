import argparse

def command1(args):
    # Logic for command 1
    print("Running command 1 with arguments:", args)

def command2(args):
    # Logic for command 2
    print("Running command 2 with arguments:", args)

def main():
    parser = argparse.ArgumentParser(description='My Backend CLI')

    subparsers = parser.add_subparsers(title='Commands', dest='command')
    
    # Command 1
    parser_command1 = subparsers.add_parser('command1', help='Description of command 1')
    parser_command1.add_argument('arg1', help='Argument for command 1')
    parser_command1.set_defaults(func=command1)

    # Command 2
    parser_command2 = subparsers.add_parser('command2', help='Description of command 2')
    parser_command2.add_argument('arg2', help='Argument for command 2')
    parser_command2.set_defaults(func=command2)

    while True:
        # Prompt for user input
        user_input = input('Enter a command (or "quit" to exit): ')
        if user_input == 'quit':
            break

        # Parse the user input
        args = parser.parse_args(user_input.split())

        # Execute the corresponding command function
        if hasattr(args, 'func'):
            args.func(args)
        else:
            parser.print_help()

if __name__ == '__main__':
    main()
