extern "C" {
#include "openaptx.h"
#include "ubertooth.h"
#include "ubertooth_fifo.h"
}

/* FIXME: where was this copied from? where should it be moved to? */
#define BULK_OUT_EP 0x05

/* TODO:
   1. (transmitter end) hook up the ubertooth lifecycle methods (as seen in
   ubertooth-specan.c) to write random data (technically pcm) and use the other
   laptop to analyze the spectrum to see that stuff is happening!
   DONE: run ./pants binary aptx-transmission:bin && sudo
   LD_LIBRARY_PATH="$(pwd)/host/libubertooth/src" ./dist/bin.pex
   2. make it work on osx!
   3. (receiver end) try to decode and pull pcm data from the device to pipe
   somewhere (use sox as in the libopenaptx README!).
*/

#define _aptx_die(var, expr)                                                   \
  if (((var) = (expr)) < 0) {                                                  \
    return (var);                                                              \
  }

namespace ubertooth_wrapper {
bool tx_aaaaaa(ubertooth_t *ut) {
  constexpr size_t len = 64;
  uint8_t tx_arr[len];
  for (size_t i = 0; i < 64; i++) {
    auto num_transferred =
        libusb_bulk_transfer(ut->devh, BULK_OUT_EP, tx_arr, len, nullptr, 100);
    /* if (num_transferred < len) { */
    /*   return false; */
    /* } */
    if (num_transferred == 0) {
      return false;
    }
  }
  return true;
  /* while (fifo_push_multiple(ut->fifo, &tx, 1)) { */
}
/*   /\* } *\/ */
/* } */
} // namespace ubertooth_wrapper

extern "C" int transmit_aptx_hd(int ubertooth_device) {
  auto aptx_hd_ctx = aptx_init(1);
  auto ut = ubertooth_start(ubertooth_device);
  int r = 0;
  _aptx_die(r, ubertooth_check_api(ut));
  register_cleanup_handler(ut, 0);
  _aptx_die(r, ubertooth_bulk_init(ut));
  _aptx_die(r, ubertooth_bulk_thread_start());
  _aptx_die(r, cmd_set_usrled(ut->devh, 0));
  _aptx_die(r, cmd_set_rxled(ut->devh, 0));
  _aptx_die(r, cmd_set_txled(ut->devh, 1));
  _aptx_die(r, cmd_tx_syms(ut->devh));

  while (!ut->stop_ubertooth && ubertooth_wrapper::tx_aaaaaa(ut)) {
  }

  ubertooth_bulk_thread_stop();
  ubertooth_stop(ut);
  aptx_finish(aptx_hd_ctx);
  return r;
}

extern "C" int add_three(int x) { return x + 3; }
