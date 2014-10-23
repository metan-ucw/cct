#include <stdio.h>
#include "link_list.h"

const char *words[] = {
	"All",
	"acts",
	"are",
	"impermanent",
	"That",
	"is",
	"the",
	"law",
	"of",
	"creation",
	"and",
	"destruction",
	"When",
	"all",
	"creation",
	"destruction",
	"are",
	"extinguished",
	"That",
	"ultimate",
	"stillness",
	"is",
	"true",
	"bliss",
	NULL,
};

static void print(struct word *list)
{
	struct word *i;

	for (i = list; i; i = i->next)
		printf("%s\n", i->word);
}

int main(void)
{
	unsigned int i;
	struct word buf[100], *root = NULL;

	for (i = 0; words[i]; i++) {
		buf[i].word = words[i];
		wordlist_push(&root, &buf[i]);
	}

	wordlist_sort(&root);

	print(root);

	//wordlist_destroy(&root);

	return 0;
}
