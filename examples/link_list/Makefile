all: list

list: list.c link_list.c link_list.h

link_list.h: link_list.h.t link_list.t
link_list.c: link_list.c.t link_list.t

clean:
	rm -f link_list.h link_list.c list

%.c: %.c.t
	../../cct.py $<

%.h: %.h.t
	../../cct.py $<
