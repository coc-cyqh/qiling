#!/usr/bin/env python3
#
# Cross Platform and Multi Architecture Advanced Binary Emulation Framework
#



from .render import *
from ..arch import ArchARM, ArchCORTEX_M

class ContextRenderARM(ContextRender, ArchARM):
    """
    context render for ARM
    """

    def __init__(self, ql, predictor):
        super().__init__(ql, predictor)
        ArchARM.__init__(self)
        self.disasm_num = 8

    @staticmethod
    def print_mode_info(bits):
        flags = ArchARM.get_flags(bits)

        print(f"[{flags.pop('mode')} mode] ", end="")
        for key, val in flags.items():
            if val:
                print(f"{color.BLUE}{key.upper()} ", end="")
            else:
                print(f"{color.GREEN}{key.lower()} ", end="")

        print(color.END)

    @Render.divider_printer("[ REGISTERS ]")
    def context_reg(self, saved_reg_dump):
        """
        redering context registers
        """

        cur_regs = self.dump_regs()
        cur_regs = self.swap_reg_name(cur_regs)
        diff_reg = self.reg_diff(cur_regs, saved_reg_dump)
        self.render_regs_dump(cur_regs, diff_reg=diff_reg)
        self.print_mode_info(self.ql.arch.regs.cpsr)



class ContextRenderCORTEX_M(ContextRenderARM, ArchCORTEX_M):
    """
    context render for cortex_m
    """

    def __init__(self, ql, predictor):
        super().__init__(ql, predictor)
        ArchCORTEX_M.__init__(self)
        self.regs_a_row = 3

    @Render.divider_printer("[ REGISTERS ]")
    def context_reg(self, saved_reg_dump):
        cur_regs = self.dump_regs()
        cur_regs = self.swap_reg_name(cur_regs)

        # for re-order
        extra_dict = {
                "xpsr": "xpsr",
                "control": "control",
                "primask": "primask",
                "faultmask": "faultmask",
                "basepri": "basepri",
                }

        cur_regs = self.swap_reg_name(cur_regs, extra_dict=extra_dict)
        diff_reg = self.reg_diff(cur_regs, saved_reg_dump)
        self.render_regs_dump(cur_regs, diff_reg=diff_reg)
        self.print_mode_info(self.ql.arch.regs.cpsr)
