/*
 * Restart after a firmware crash instead of halting. The XIAO reset buttons
 * sit inside the case, so a halted half could not otherwise be recovered.
 */

#include <zephyr/fatal.h>
#include <zephyr/sys/reboot.h>

void k_sys_fatal_error_handler(unsigned int reason, const struct arch_esf *esf) {
    ARG_UNUSED(reason);
    ARG_UNUSED(esf);

    sys_reboot(SYS_REBOOT_COLD);
}
