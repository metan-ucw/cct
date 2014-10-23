@ include source.t
@ include link_list.t
@ import list
#include <stdlib.h>
#include "link_list.h"

@ for list in list.list_descs:
@     genlist_source(list)
