all: header.h

clean:
	rm -f header.h

%.h: %.h.t
	../../cct.py $<
