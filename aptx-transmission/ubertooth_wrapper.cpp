extern "C" {
#include "openaptx.h"
#include "ubertooth.h"
}

/* TODO:
   1. (transmitter end) hook up the ubertooth lifecycle methods (as seen in ubertooth-specan.c) to
      write random data (technically pcm) and use the other laptop to analyze the spectrum to see
      that stuff is happening!
   2. make it work on osx!
   3. (receiver end) try to decode and pull pcm data from the device to pipe somewhere (use sox as
      in the libopenaptx README!).
*/

extern "C" void transmit_aptx_hd() {
  auto ctx = aptx_init(1);
  aptx_finish(ctx);
}

extern "C" int add_three(int x) { return x + 3; }
