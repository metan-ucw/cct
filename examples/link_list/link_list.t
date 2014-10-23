@ def genlist_source(list):
void {{ list.prefix }}_push(struct {{ list.struct }} **root, struct {{ list.struct }} *elem)
{
	elem->{{ list.next }} = *root;
@     if list.prev:
	elem->{{ list.prev }} = NULL;

	if (*root) {
		(*root)->{{ list.prev }} = elem;
	}
@     end

	*root = elem;
}

struct {{ list.struct }} *{{ list.prefix }}_pop(struct {{ list.struct }} **root)
{
	struct {{ list.struct }} *elem = *root;

	if (*root) {
		*root = (*root)->{{ list.next }};
@     if list.prev:
		if (*root)
			(*root)->{{ list.prev }} = NULL;
@     end
	}

	return elem;
}

@     if list.compare:
static void {{ list.prefix }}_mergesort(struct {{ list.struct }} **root)
{
	struct {{ list.struct }} *tmp, *middle, *pre_middle, *start;

	if (!*root || !(*root)->{{ list.next }})
		return;

	start = *root;

	/* Find middle of the list */
	for (middle = tmp = start; tmp != NULL; tmp = tmp->{{ list.next }}) {
		pre_middle = middle;
		middle = middle->{{ list.next }};
		if (tmp->{{ list.next }})
			tmp = tmp->{{ list.next }};
	}

	pre_middle->{{ list.next }} = NULL;

	{{ list.prefix }}_mergesort(&start);
	{{ list.prefix }}_mergesort(&middle);

	if ({{ list.compare('start', 'middle') }}) {
		*root = tmp = start;
		start = start->{{ list.next }};
	} else {
		*root = tmp = middle;
		middle = middle->{{ list.next }};
	}

	while (start || middle) {
		while (start && (!middle || {{ list.compare('start', 'middle') }})) {
			tmp->{{ list.next }} = start;
			tmp = start;
			start = start->{{ list.next }};
		}

		while (middle && (!start || !{{ list.compare('start', 'middle') }})) {
			tmp->{{ list.next }} = middle;
			tmp = middle;
			middle = middle->{{ list.next }};
		}
	}

	tmp->{{ list.next }} = NULL;
}

void {{ list.prefix }}_sort(struct {{ list.struct }} **root)
{
	{{ list.prefix }}_mergesort(root);
@         if list.prev:

	struct {{ list.struct }} *tmp = *root;

	if (tmp)
		tmp->{{ list.prev }} = NULL;

	for (; tmp; tmp = tmp->{{ list.prev }}) {
		if (tmp->{{ list.next }})
			tmp->{{ list.next }}->{{ list.prev }} = tmp;
	}
@         end
}
@     end
@
@     if list.free:
void {{ list.prefix }}_destroy(struct {{ list.struct }} **root)
{
	struct {{ list.struct }} *i, *tmp;

	if (!root || !*root)
		return;

	for (i = *root, *root = NULL; i;) {
		tmp = i;
		i = i->{{ list.next }};
		{{ list.free('tmp') }};
	}
}
@     end

@ end
@ def genlist_header(list):
void {{ list.prefix }}_push(struct {{ list.struct }} **root, struct {{ list.struct }} *elem);

struct {{ list.struct }} *{{ list.prefix }}_pop(struct {{ list.struct }} **root);

void {{ list.prefix }}_sort(struct {{ list.struct }} **root);

void {{ list.prefix }}_destroy(struct {{ list.struct }} **root);
@ end
