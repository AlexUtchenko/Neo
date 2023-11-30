def formatted_numbers():
    print('|{:^10}|{:^10}|{:^10}|'.format('decimal', 'hex', 'binary'))
    for i in range(1,16):
        print('|{:<10d}|{:^10x}|{:>10b}|'.format(i, i, i))

formatted_numbers()