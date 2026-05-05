LIBS_DIR := ../pibody_libs
FS_OFFSET := 0x1012C000
BUILD_DIR := ./build

all: firmware.uf2 filesystem.uf2
	python merge_uf2.py firmware.uf2 filesystem.uf2 pibody.uf2

filesystem.uf2: filesystem.bin
	python uf2conv.py --base $(FS_OFFSET) --family rp2040 --output $@ $<

filesystem.bin:
	python make_fs.py $(LIBS_DIR)

clean:
	rm -f filesystem.bin filesystem.uf2 combined.uf2