@ include header.t
@ include link_list.t
@ import list
@
struct word {
	struct word *next;
	struct word *prev;

	const char *word;
};

@ for list in list.list_descs:
@     genlist_header(list)

