class list_desc:
    def __init__(self, struct, next, prev, prefix, compare, free):
        self.struct = struct
        self.next = next
        self.prev = prev
        self.prefix = prefix
        self.compare = compare
        self.free = free

list_descs = [
        list_desc('word', 'next', 'prev', 'wordlist',
                  lambda x, y: '(strcmp(' + x + '->word, ' + y + '->word) > 0)',
                  lambda x: 'free(' + x + ')'),
];

