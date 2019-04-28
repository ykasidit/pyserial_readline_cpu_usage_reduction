pyserial_readline_cpu_usage_reduction
=====================================

When used in a 'Raspbarry Pi Zero W' - I found that pyserial's `readline()` was using way too much CPU percent (as shown in 'htop') - apx 65% CPU usage for just reading NMEA from a USB GPS/GNSS Receiver (during R&D of my [EcoDroidGPS Bluetooth GPS](https://www.clearevo.com/ecodroidgps) hobby project).

This repo contains some test code that when used with `strace` would demonstrate and show what it was doing and what workaround helped reduce CPU usage.

Used pyserial version as shown in `pip list` was: `pyserial (3.4)`

Make sure you have `strace` installed. (`sudo apt-get install strace`) and have a serial device (like a USB GPS Receiver) connected and populating `/dev/ttyACM0` if you want to try the steps below yourself.


Step 1
------

Let's try run below command and see the CPU usage.

`python test_pyserial_readline.py --dev /dev/ttyACM0`

This showed apx 65% CPU in `htop`.

So let's `strace` it:

`strace -ff -F -tt -x python test_pyserial_readline.py --dev /dev/ttyACM0`

**Output:** (During reads, after load of the libs)

`
03:37:53.018796 gettimeofday({tv_sec=1556419073, tv_usec=19018}, NULL) = 0
03:37:53.019407 gettimeofday({tv_sec=1556419073, tv_usec=29665}, NULL) = 0
03:37:53.030019 _newselect(5, [3 4], [], [], {tv_sec=2, tv_usec=989352}) = 1 (in [3], left {tv_sec=2, tv_usec=989317})
03:37:53.030653 read(3, "$", 1)         = 1
03:37:53.039805 gettimeofday({tv_sec=1556419073, tv_usec=40007}, NULL) = 0
03:37:53.040429 gettimeofday({tv_sec=1556419073, tv_usec=40623}, NULL) = 0
03:37:53.040902 gettimeofday({tv_sec=1556419073, tv_usec=41075}, NULL) = 0
03:37:53.041337 _newselect(5, [3 4], [], [], {tv_sec=2, tv_usec=999547}) = 1 (in [3], left {tv_sec=2, tv_usec=999516})
03:37:53.041943 read(3, "G", 1)         = 1
03:37:53.042436 gettimeofday({tv_sec=1556419073, tv_usec=42611}, NULL) = 0
03:37:53.042999 gettimeofday({tv_sec=1556419073, tv_usec=43189}, NULL) = 0
03:37:53.043473 gettimeofday({tv_sec=1556419073, tv_usec=43647}, NULL) = 0
03:37:53.043901 _newselect(5, [3 4], [], [], {tv_sec=2, tv_usec=999541}) = 1 (in [3], left {tv_sec=2, tv_usec=999513})
03:37:53.044490 read(3, "N", 1)         = 1
03:37:53.046038 gettimeofday({tv_sec=1556419073, tv_usec=46230}, NULL) = 0
03:37:53.046636 gettimeofday({tv_sec=1556419073, tv_usec=49418}, NULL) = 0
03:37:53.049790 gettimeofday({tv_sec=1556419073, tv_usec=49988}, NULL) = 0
03:37:53.050256 _newselect(5, [3 4], [], [], {tv_sec=2, tv_usec=999429}) = 1 (in [3], left {tv_sec=2, tv_usec=999400})
03:37:53.050862 read(3, "G", 1)         = 1
03:37:53.051356 gettimeofday({tv_sec=1556419073, tv_usec=51527}, NULL) = 0
03:37:53.051920 gettimeofday({tv_sec=1556419073, tv_usec=59529}, NULL) = 0
03:37:53.059903 gettimeofday({tv_sec=1556419073, tv_usec=60103}, NULL) = 0
03:37:53.069556 _newselect(5, [3 4], [], [], {tv_sec=2, tv_usec=999426}) = 1 (in [3], left {tv_sec=2, tv_usec=999395})
03:37:53.070241 read(3, "S", 1)         = 1
`

**Observation**

Pyserial seems to read byte by byte from the device and frequently checking the time.

Step 2
------

Lets try the same as step 1 but without the timeout:

**Test Command:**
`strace -ff -F -tt -x python test_pyserial_readline.py --dev /dev/ttyACM0 --timeout_secs None`

**Output:**

`
03:46:27.967917 _newselect(5, [3 4], [], [], NULL) = 1 (in [3])
03:46:27.968482 read(3, "1", 1)         = 1
03:46:27.969207 _newselect(5, [3 4], [], [], NULL) = 1 (in [3])
03:46:27.969879 read(3, "9", 1)         = 1
03:46:27.970616 _newselect(5, [3 4], [], [], NULL) = 1 (in [3])
03:46:28.025637 read(3, ",", 1)         = 1
03:46:28.026305 _newselect(5, [3 4], [], [], NULL) = 1 (in [3])
03:46:28.026888 read(3, "2", 1)         = 1
03:46:28.027546 _newselect(5, [3 4], [], [], NULL) = 1 (in [3])
03:46:28.028106 read(3, "1", 1)         = 1
03:46:28.028754 _newselect(5, [3 4], [], [], NULL) = 1 (in [3])
03:46:28.039964 read(3, ",", 1)         = 1
03:46:28.040693 _newselect(5, [3 4], [], [], NULL) = 1 (in [3])
03:46:28.041276 read(3, "7", 1)         = 1
03:46:28.041943 _newselect(5, [3 4], [], [], NULL) = 1 (in [3])
03:46:28.042514 read(3, "3", 1)         = 1
03:46:28.043185 _newselect(5, [3 4], [], [], NULL) = 1 (in [3])
03:46:28.043753 read(3, ",", 1)         = 1
03:46:28.044410 _newselect(5, [3 4], [], [], NULL) = 1 (in [3])
03:46:28.044970 read(3, "0", 1)         = 1
03:46:28.045633 _newselect(5, [3 4], [], [], NULL) = 1 (in [3])
03:46:28.046189 read(3, "3", 1)         = 1
03:46:28.046837 _newselect(5, [3 4], [], [], NULL) = 1 (in [3])
03:46:28.047402 read(3, ",", 1)         = 1
03:46:28.048067 _newselect(5, [3 4], [], [], NULL) = 1 (in [3])
03:46:28.048632 read(3, "2", 1)         = 1
03:46:28.049417 _newselect(5, [3 4], [], [], NULL) = 1 (in [3])
03:46:28.050000 read(3, "7", 1)         = 1
03:46:28.050670 _newselect(5, [3 4], [], [], NULL) = 1 (in [3])
03:46:28.051239 read(3, "7", 1)         = 1
03:46:28.060016 _newselect(5, [3 4], [],) = 1 (in [3])
`

**Observation:** So now its not checking the with `gettimeofday()` but still reading byte by byte which still causes high CPU when run without strace - apx 45% to 55% CPU as shown in `htop`.

Step 3
------

Let's try the `read()` command as this seems to probably map directly with the native `ssize_t read(int fd, void *buf, size_t count);` command from Python's `os.read()` in pyserial's soruce code (as far as I remember).

So let's try run below command and see the CPU usage.

`python test_pyserial_readline.py --dev /dev/ttyACM0 --timeout_secs None --eval_read_code 'read(256)'`

This is much better - **showed apx 2% CPU** or less in `htop`.

Let's strace it:

`strace -ff -F -tt -x python test_pyserial_readline.py --dev /dev/ttyACM0 --timeout_secs None --eval_read_code 'read(256)'`

**Output:**

`
03:58:27.120054 read(3, "4,33,05,26,154,18,08,41,312,32,7"..., 256) = 256
03:58:27.120946 write(1, "read string: 4,33,05,26,154,18,0"..., 217read string: 4,33,05,26,154,18,08,41,312,32,7*7A
$GAGSV,3,2,09,11,06,061,,15,01,208,,25,13,036,,30,23,287,,7*7A
$GAGSV,3,3,09,36,31,106,21,7*49
$GAGSV,3,1,09,02,34,344,19,03,74,204,25,05,26,154,,08,41,312,24,2*78
) = 217
03:58:27.121614 write(1, "$GAGSV,3,2,09,11,06,061,,15,01,2"..., 53$GAGSV,3,2,09,11,06,061,,15,01,208,,25,13,036,,30,23
) = 53
03:58:27.123010 _newselect(5, [3 4], [], [], NULL) = 1 (in [3])
03:58:27.123878 read(3, ",287,,2*7F\r\n$GAGSV,3,3,09,36,31,"..., 256) = 256
03:58:27.124721 write(1, "read string: ,287,,2*7F\r\n$GAGSV,"..., 262read string: ,287,,2*7F
$GAGSV,3,3,09,36,31,106,19,2*47
$GBGSV,5,1,17,02,67,245,,03,77,128,,04,23,094,,05,40,260,,1*71
$GBGSV,5,2,17,06,66,143,26,07,40,008,27,08,26,145,,09,82,345,,1*70
$GBGSV,5,3,17,10,47,333,29,13,24,175,22,14,30,293,26,16,75,146,26,1*73
) = 262
03:58:27.125387 write(1, "$GBGSV,\n", 8$GBGSV,
) = 8
03:58:27.126829 _newselect(5, [3 4], [], [], NULL) = 1 (in [3])
03:58:27.127751 read(3, "5,4,17,21,53,229,37,22,25,168,,2"..., 256) = 256
03:58:27.128611 write(1, "read string: 5,4,17,21,53,229,37"..., 229read string: 5,4,17,21,53,229,37,22,25,168,,24,07,294,,26,28,339,,1*78
$GBGSV,5,5,17,29,17,052,,1*4A
$GBGSV,5,1,17,02,67,245,,03,77,128,,04,23,094,,05,40,260,,*40
$GBGSV,5,2,17,06,66,143,,07,40,008,,08,26,145,,09,82,345,,*40
) = 229
`

So this is using the native `read` with a max of 256 and resulting in much less CPU usage! This is what I would expect if I wrote a native C program and reading from the file descriptor.

Now, if we use the 'timeout' again like below:
`strace -ff -F -tt -x python test_pyserial_readline.py --dev /dev/ttyACM0 --timeout_secs 5 --eval_read_code 'read(256)'`

Output:
`
04:03:28.111969 _newselect(5, [3 4], [], [], {tv_sec=4, tv_usec=999333}) = 1 (in [3], left {tv_sec=4, tv_usec=999292})
04:03:28.112825 read(3, ",18,180,,6*6D\r\n$GPGSV,4,3,14,22,"..., 256) = 256
04:03:28.113494 gettimeofday({tv_sec=1556420608, tv_usec=113735}, NULL) = 0
04:03:28.114263 write(1, "read string: ,18,180,,6*6D\r\n$GPG"..., 210read string: ,18,180,,6*6D
$GPGSV,4,3,14,22,32,212,,23,43,328,,26,15,030,19,27,69,082,30,6*66
$GPGSV,4,4,14,31,15,078,17,32,09,142,,6*66
$GLGSV,3,1,09,68,24,173,32,69,59,229,28,70,30,311,26,73,04,286,,1*70
) = 210
04:03:28.114924 write(1, "$GLGSV,3,2,09,79,10,031,23,80,19"..., 60$GLGSV,3,2,09,79,10,031,23,80,19,340,28,81,15,051,24,82,40,
) = 60
04:03:28.116219 gettimeofday({tv_sec=1556420608, tv_usec=116528}, NULL) = 0
04:03:28.116952 gettimeofday({tv_sec=1556420608, tv_usec=117200}, NULL) = 0
04:03:28.117588 _newselect(5, [3 4], [], [], {tv_sec=4, tv_usec=999328}) = 1 (in [3], left {tv_sec=4, tv_usec=999288})
04:03:28.118450 read(3, "100,30,1*72\r\n$GLGSV,3,3,09,83,28"..., 256) = 256
04:03:28.119133 gettimeofday({tv_sec=1556420608, tv_usec=119494}, NULL) = 0
04:03:28.120048 write(1, "read string: 100,30,1*72\r\n$GLGSV"..., 230read string: 100,30,1*72
$GLGSV,3,3,09,83,28,162,20,1*47
$GLGSV,3,1,09,68,24,173,09,69,59,229,28,70,30,311,,73,04,286,,3*7E
$GLGSV,3,2,09,79,10,031,17,80,19,340,16,81,15,051,08,82,40,100,23,3*76
$GLGSV,3,3,09,83,28,162,,3*47
) = 230
04:03:28.129879 write(1, "$GAGSV,3,1,09,02,34,346,36,03,73"..., 40$GAGSV,3,1,09,02,34,346,36,03,73,202,28
) = 40
04:03:28.131229 gettimeofday({tv_sec=1556420608, tv_usec=131535}, NULL) = 0
04:03:28.131956 gettimeofday({tv_sec=1556420608, tv_usec=132200}, NULL) = 0
`

CPU Usage is still apx the same so it's ok to use a timeout check here.


Step 4
------

Of course, in step 3 we lost our 'readline()' functionality while getting much better CPU efficiency. So let's add this functionality via the `io.BufferedReader` class to wrap/buffer over our pyserial object (the BufferedReader would only call `read()` as it expects a raw io interface not having readline() which it would provide itself).

Test code:
`python test_pyserial_readline.py --dev /dev/ttyACM0 --timeout_secs None --eval_read_code 'readline(256)' --eval_pyserial_post_setup_code 'io.BufferedReader(serial_obj, buffer_size=256)'`

Ok! Now `htop` is showing apx 2-5% CPU only! And we got our readline() functionality back!!!

Let's strace it to see how the `BufferedReader` is using `read()`:
`strace -ff -F -tt -s 500  python test_pyserial_readline.py --dev /dev/ttyACM0 --timeout_secs None --eval_read_code 'readline(256)' --eval_pyserial_post_setup_code 'io.BufferedReader(serial_obj, buffer_size=256)'`

Output:

<pre>
04:27:21.161158 _newselect(5, [3 4], [], [], NULL) = 1 (in [3])
04:27:22.057035 read(3, "$GNRMC,032722.00,A,0641.64224,N,10137.05668,E,0.033,,280419,,,A,V*18\r\n$GNVTG,,T,,M,0.033,N,0.061,K,A*3A\r\n", 256) = 105
04:27:22.057950 _newselect(5, [3 4], [], [], NULL) = 1 (in [3])
04:27:22.059696 read(3, "$GNGGA,032722.00,0641.64224,N,10137.05668,E,1,12,0.51,29.1,M,-13.0,M,,*5A\r\n$GNGSA,A,3,11,03,22,01,18,16,23,08,31,27,,,1.09,0.51,0.96,1*00\r\n$GNGSA,A,3,8", 151) = 151
04:27:22.069538 write(1, "read string: $GNRMC,032722.00,A,0641.64224,N,10137.05668,E,0.033,,280419,,,A,V*18\r\n", 83read string: $GNRMC,032722.00,A,0641.64224,N,10137.05668,E,0.033,,280419,,,A,V*18
) = 83
04:27:22.070084 write(1, "\n", 1
)       = 1
04:27:22.071096 write(1, "read string: $GNVTG,,T,,M,0.033,N,0.061,K,A*3A\r\n", 48read string: $GNVTG,,T,,M,0.033,N,0.061,K,A*3A
) = 48
04:27:22.071619 write(1, "\n", 1
)       = 1
04:27:22.072589 write(1, "read string: $GNGGA,032722.00,0641.64224,N,10137.05668,E,1,12,0.51,29.1,M,-13.0,M,,*5A\r\n", 88read string: $GNGGA,032722.00,0641.64224,N,10137.05668,E,1,12,0.51,29.1,M,-13.0,M,,*5A
) = 88
04:27:22.073095 write(1, "\n", 1
)       = 1
04:27:22.074041 write(1, "read string: $GNGSA,A,3,11,03,22,01,18,16,23,08,31,27,,,1.09,0.51,0.96,1*00\r\n", 77read string: $GNGSA,A,3,11,03,22,01,18,16,23,08,31,27,,,1.09,0.51,0.96,1*00
) = 77
04:27:22.074553 write(1, "\n", 1
)       = 1
04:27:22.075616 _newselect(5, [3 4], [], [], NULL) = 1 (in [3])
04:27:22.076257 read(3, "0,82,69,70,,,,,,,,,1.09,0.51,0.96,2*0B\r\n$GNGSA,A,3,08,36,03,02,05,,,,,,,,1.09,0.51,0.96,3*09\r\n$GNGSA,A,3,14,07,10,06,13,21,,,,,,,1.09,0.51,0.96,4*03\r\n$GPGSV,4,1,15,01,11,195,22,03,30,225,35,07,02,312,,08,74,181,27,1*69\r\n$GPGSV,4,2,15,09,18,324,,11,26,189,3", 256) = 256
04:27:22.076962 write(1, "read string: $GNGSA,A,3,80,82,69,70,,,,,,,,,1.09,0.51,0.96,2*0B\r\n", 65read string: $GNGSA,A,3,80,82,69,70,,,,,,,,,1.09,0.51,0.96,2*0B
) = 65
04:27:22.077461 write(1, "\n", 1
)       = 1
04:27:22.090081 write(1, "read string: $GNGSA,A,3,08,36,03,02,05,,,,,,,,1.09,0.51,0.96,3*09\r\n", 67read string: $GNGSA,A,3,08,36,03,02,05,,,,,,,,1.09,0.51,0.96,3*09
) = 67
04:27:22.090615 write(1, "\n", 1
)       = 1
04:27:22.091563 write(1, "read string: $GNGSA,A,3,14,07,10,06,13,21,,,,,,,1.09,0.51,0.96,4*03\r\n", 69read string: $GNGSA,A,3,14,07,10,06,13,21,,,,,,,1.09,0.51,0.96,4*03
) = 69
04:27:22.092068 write(1, "\n", 1
)       = 1
04:27:22.093024 write(1, "read string: $GPGSV,4,1,15,01,11,195,22,03,30,225,35,07,02,312,,08,74,181,27,1*69\r\n", 83read string: $GPGSV,4,1,15,01,11,195,22,03,30,225,35,07,02,312,,08,74,181,27,1*69
) = 83
04:27:22.093545 write(1, "\n", 1
)       = 1
04:27:22.094653 _newselect(5, [3 4], [], [], NULL) = 1 (in [3])
04:27:22.095321 read(3, "0,14,16,142,07,16,27,015,26,1*64\r\n$GPGSV,4,3,15,18,22,171,19,22,27,202,31,23,53,322,31,26,09,037,18,1*60\r\n$GPGSV,4,4,15,27,64,054,39,31,14,089,22,32,00,145,,1*5B\r\n$GPGSV,4,1,15,01,11,195,23,03,30,225,23,07,02,312,,08,74,181,20,6*6F\r\n$GPGSV,4,2,15,09,18,324", 256) = 256
04:27:22.096029 write(1, "read string: $GPGSV,4,2,15,09,18,324,,11,26,189,30,14,16,142,07,16,27,015,26,1*64\r\n", 83read string: $GPGSV,4,2,15,09,18,324,,11,26,189,30,14,16,142,07,16,27,015,26,1*64
) = 83
04:27:22.096530 write(1, "\n", 1
)       = 1
04:27:22.097525 write(1, "read string: $GPGSV,4,3,15,18,22,171,19,22,27,202,31,23,53,322,31,26,09,037,18,1*60\r\n", 85read string: $GPGSV,4,3,15,18,22,171,19,22,27,202,31,23,53,322,31,26,09,037,18,1*60
) = 85
04:27:22.098044 write(1, "\n", 1
)       = 1
04:27:22.099016 write(1, "read string: $GPGSV,4,4,15,27,64,054,39,31,14,089,22,32,00,145,,1*5B\r\n", 70read string: $GPGSV,4,4,15,27,64,054,39,31,14,089,22,32,00,145,,1*5B
) = 70
04:27:22.099633 write(1, "\n", 1
)       = 1
04:27:22.100627 write(1, "read string: $GPGSV,4,1,15,01,11,195,23,03,30,225,23,07,02,312,,08,74,181,20,6*6F\r\n", 83read string: $GPGSV,4,1,15,01,11,195,23,03,30,225,23,07,02,312,,08,74,181,20,6*6F
) = 83
04:27:22.101148 write(1, "\n", 1
)       = 1
</pre>

OK, this seems clean enough! Not sure if the timeout functionality is still there or not though - should be but I'm too lazy to verify that today ;-)


My humble conclusion
--------------------

I'd avoid using pyserial's `readline()`, especially in less powerful devices where CPU power is quite limited, I'd use its `read()` function instead, and if we really need `readline()` we could use `io.BufferedReader` to wrap over the pyserial object where total CPU usage dropped from apx 60% to apx 5% in the Raspberry Pi Zero W (or write a buffering and `\n` splitter function if you like of course...).

Another working method was calling readline() from the piped `stdout` of `subprocess` that called `busybox microcom -s 115200 /dev/ttyACM0` but that created a subprocess and we probably have less control/connection to the direct io or fd should issues arise, or another way would be to write a C .so lib or a Cython .so lib that would do the native reads and readlines but that was a overkill I think as above solution seems already good enough.

Thanks for reading and hope this helps reduce CPU usage for someone doing pyserial reads!