CC=gcc -Wall
CFLAGS=-I. -D'proc_name="tcu"' -D'version="0.1b"'

SRCS=$(wildcard ./src/*.c)
OBJS = $(SRCS:.c=.o)

OUTPUT = tcu
LIBS=-lwiringPi -pthread -lcrypt -lm -lrt

# -----------------------------------------------

TARGET_DIR="/opt/tcu"
SYSTEMD_DIR="/lib/systemd/system"

# -----------------------------------------------

all: main

# -----------------------------------------------

%.o: %.c
	$(CC) -c -o $@ $< $(CFLAGS)

main: $(OBJS)
	gcc -o $(OUTPUT) $^ $(CFLAGS) $(LIBS)

# -----------------------------------------------

install: main
	mkdir -p $(TARGET_DIR)
	cp $(OUTPUT) $(TARGET_DIR)
	cp -r config/ $(TARGET_DIR)
	cp -r systemd/ $(TARGET_DIR)
	cp $(TARGET_DIR)/systemd/tcu.service $(SYSTEMD_DIR)
	systemctl daemon-reload

remove:
	systemctl stop tcu.service
	rm -r $(TARGET_DIR)
	rm $(SYSTEMD_DIR)/tcu.service
	systemctl daemon-reload

# -----------------------------------------------

.PHONY: clean

clean:
	rm -f $(OBJS) *~ $(OUTPUT) $(INCDIR)/*~
