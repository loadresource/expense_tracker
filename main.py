import source.sysargs as sysargs

def main():
    parser = sysargs.create_parser()
    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        print("No command provided. Use -h for help.")
        parser.print_help()
    
if __name__ == "__main__":
    main()
