# Linker Map Summary
Summarizes the size of objects linked into a binary based on a linker map
generated by GNU ld with --print-map (should work on all platforms), by summing
together portions in sections spread throughout the binary.
This is useful to see the size impact of different portions of code after the
linker has dropped unneeded sections.

Requires python 2.7+ or 3.2+.

## Use
`python analyze_map.py [--combine] firmware.elf.map`

## Example Output
```
/usr/local/Cellar/arm-none-eabi-gcc/20150921/arm-none-eabi/lib/armv6-m/libm.a(lib_a-kf_rem_pio2.o) 	1888
build-arduino_zero/py/mpprint.o 	1938
build-arduino_zero/py/objset.o 	2018
build-arduino_zero/py/obj.o 	2038
build-arduino_zero/py/objarray.o 	2122
build-arduino_zero/boards/arduino_zero/pins.o 	2144
build-arduino_zero/py/objdict.o 	2146
build-arduino_zero/py/objlist.o 	2210
build-arduino_zero/py/lexer.o 	2405
build-arduino_zero/py/objexcept.o 	2466
build-arduino_zero/asf/sam0/drivers/usb/stack_interface/usb_device_udd.o 	2692
build-arduino_zero/asf/sam0/drivers/usb/usb_sam_d_r/usb.o 	3026
build-arduino_zero/py/emitbc.o 	3166
build-arduino_zero/py/modbuiltins.o 	3219
build-arduino_zero/py/gc.o 	3411
build-arduino_zero/py/objtype.o 	3579
build-arduino_zero/py/vm.o 	4259
build-arduino_zero/py/runtime.o 	4627
build-arduino_zero/py/parse.o 	4676
build-arduino_zero/py/qstr.o 	6589
build-arduino_zero/py/objstr.o 	9070
build-arduino_zero/lib/fatfs/ff.o 	10777
build-arduino_zero/py/compile.o 	11731
```

An example with --combine:
```
c:/mingw/lib/libshell32.a 	32
c:/mingw/lib/libadvapi32.a 	48
c:/mingw/lib/libmoldname.a 	64
C:\Program Files\FreeBASIC\lib\win32\*.o 	80
c:/mingw/lib/libgdi32.a 	160
c:/mingw/lib/gcc/mingw32/4.8.1/*.o 	520
win32/libSDL.dll.a 	544
c:/mingw/lib/libuser32.a 	896
c:/mingw/lib/*.o 	1536
c:/mingw/lib/libmsvcrt.a 	1680
c:/mingw/lib/libkernel32.a 	1744
build\lib\SDL\*.o 	1984
c:/mingw/lib/gcc/mingw32/4.8.1/libgcc.a 	4952
c:/mingw/lib/libmingw32.a 	5696
c:/mingw/lib/gcc/mingw32/4.8.1/libgcc_eh.a 	33408
c:/mingw/lib/libmingwex.a 	53080
c:/mingw/lib/gcc/mingw32/4.8.1\libstdc++.a 	63376
C:\Program Files\FreeBASIC\lib\win32/libfbmt.a 	166992
build\lib\*.o 	229856
build\*.o 	4149088
```
